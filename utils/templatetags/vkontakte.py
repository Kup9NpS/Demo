from django import template
from utils import vkontakte


register = template.Library()


@register.simple_tag(takes_context=True)
def vkontakte_auto_auth_link(context):
    return vkontakte.build_login_link(context['request'].path)


@register.simple_tag
def vkontakte_auth_link(redirect_uri):
    return vkontakte.build_login_link(redirect_uri)


@register.simple_tag
def vkontakte_profile_link(vkuserid):
    vkuserid = str(vkuserid)
    return 'http://vk.com/' + 'id' * vkuserid.isdigit() + vkuserid