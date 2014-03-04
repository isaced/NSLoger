# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from bbs.models import Notice
import markdown2

register = template.Library()

# --- tag ---

@register.simple_tag
def notice_set_all_readed(user):
    Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).update(is_readed=True)
    return ''

@register.simple_tag
def num_notice(user):
    num = Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).count()
    return num

# --- filter ---

@register.filter(is_safe=True)
@stringfilter
def my_markdown(value):
	return mark_safe(markdown2.markdown(force_unicode(value),extras=['fenced-code-blocks'],safe_mode=True))