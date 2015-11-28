# coding=utf-8
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
import re, random

register = template.Library()


@register.inclusion_tag('tagtemplates/avatar.html')
def avatar(avatar_field, size='30', circle=False, sex='m', thumbnail='False'):
    size = str(size)
    return {'avatar_field': avatar_field, 'circle': circle, 'size': size + 'x' + size, 'side_size': size, 'sex': sex, 'thumbnail': thumbnail}


@register.inclusion_tag('tagtemplates/image.html')
def image(image, width='30', height='', thumbnail='False'):
    x = str(width)
    y = str(height)
    return {'img': image, 'size': x + 'x' + y, 'side_size': x, 'thumbnail': thumbnail}


# Определяет активный пункт меню
@register.simple_tag(takes_context=True)
def active(context, urlname):
    try:
        pattern = '^' + reverse(urlname)
    except NoReverseMatch:
        pattern = urlname
    path = context.get('request').path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.simple_tag
def random_choice(*args):
    return random.choice(args)