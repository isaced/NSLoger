# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from bbs.models import Notice,FavoritedTopic
from people.models import Member as User
from people.models import Follower

import markdown
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

# --------- filter ---------

#  -------- Markdown Extension --------
class CommentMarkdownExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.parser.blockprocessors['hashheader']		#删除H1~H6标签
#  -------- Markdown Extension --------

@register.filter(is_safe=True)
@stringfilter
def my_markdown(value, flag):

    extension_list = ['nl2br','fenced_code']

    # 根据参数（主题或评论）载入不同Markdown扩展
    if flag == 'comment':
        extension_list.append(CommentMarkdownExtension())

    md = markdown.markdown(force_unicode(value), extension_list, safe_mode = 'escape')
	

	# @人给链接输出
    team_name_pattern = re.compile('(?<=@)([0-9a-zA-Z.]+)', re.UNICODE)
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
