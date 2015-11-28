# coding=utf-8
__author__ = 'vitaliyharchenko'

from django import template
from events.models import UserGameAction

register = template.Library()

# TODO: create template
@register.inclusion_tag('tagtemplates/blog_post.html', takes_context=True)
def render_post(context, event):
    return True