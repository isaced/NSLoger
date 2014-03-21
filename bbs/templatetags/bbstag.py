# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from bbs.models import Notice,FavoritedTopic
from people.models import Member as User
from people.models import Follower

import datetime
from django.utils import timezone
from django.utils.translation import ugettext as _

import misaka
import re

register = template.Library()

# --- tag ---

@register.simple_tag
def notice_set_all_readed(user):
    Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).update(is_readed=True)
    return ''

@register.assignment_tag
def num_notice(user):
    num = Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).count()
    return num

@register.simple_tag
def get_fav_count(user):
    num = FavoritedTopic.objects.filter(user=user).count()
    return num

@register.simple_tag
def get_following_count(user):
    num = Follower.objects.filter(user_a=user).count()
    return num

# 计算楼层
@register.simple_tag
def page_item_idx(page_obj, p ,forloop):
	return page_obj.page(p).start_index() + forloop['counter0']

@register.filter
def time_to_now(value):
    now = timezone.now()
    delta = now - value
    if delta.days > 365:
        return '%s 年前' % str(delta.days / 365)
    if delta.days > 30:
        return '%s 月前' % str(delta.days / 30)
    if delta.days > 0:
        return '%s 天前' % str( delta.days)
    if delta.seconds > 3600:
        return '%s 小时前' % str(delta.seconds / 3600)
    if delta.seconds > 60:
        return '%s 分钟前' % str(delta.seconds / 60)
    return '刚刚'

# --------- filter ---------

#  -------- Markdown Extension --------
class BaseRenderer(misaka.HtmlRenderer):
    def autolink(self, link, is_email):
        if is_email:
            return '<a href="mailto:%(link)s">%(link)s</a>' % {'link': link}
        content = link.replace('http://', '').replace('https://', '')
        return '<a href="%s" target="_blank">%s</a>' % (link, content)

class CommentRenderer(BaseRenderer):
    def header(self, text, level):
        if level < 4:
            return '<p>#%s</p>' % text
        return '<h%d>%s</h%d>' % (level, text, level)

class TopicRenderer(BaseRenderer):
    pass
#  -------- Markdown Extension --------

@register.filter(is_safe=True)
@stringfilter
def my_markdown(value, flag):

    extensions = (
        misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_FENCED_CODE | misaka.EXT_AUTOLINK |
        misaka.EXT_TABLES | misaka.EXT_STRIKETHROUGH | misaka.EXT_SUPERSCRIPT
    )

    # 根据参数（主题或评论）载入不同Markdown扩展
    if flag == 'comment':
        renderer = CommentRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP)
    else:
        renderer = TopicRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP)

    md = misaka.Markdown(renderer, extensions=extensions)
    md = md.render(force_unicode(value))

	# @人给链接输出
    team_name_pattern = re.compile('(?<=@)([0-9a-zA-Z_.]+)', re.UNICODE)
    at_name_list = set(re.findall(team_name_pattern, md))
    if at_name_list:
		for at_name in at_name_list:
			try:
				at_user = User.objects.get(username=at_name)
				if at_user:
					md = md.replace('@'+at_name,'<a href="%s" class="at_user">@%s</a>' % (reverse("user:user",args=(at_user.id,)),at_name))
			except:
				pass

    return mark_safe(md)
