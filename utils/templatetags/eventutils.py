# coding=utf-8
__author__ = 'vitaliyharchenko'

from django import template
from events.models import UserGameAction

register = template.Library()


@register.inclusion_tag('tagtemplates/event.html', takes_context=True)
def event_pane(context, event):
    newcontext = {'event': event.as_leaf_class,
                  'current_user': context['current_user']}
    try:
        newcontext['standalone'] = context['standalone']
    except KeyError:
        pass
    return newcontext


# находит объект подписи на игру для заданной игры и пользователя
@register.assignment_tag
def usergameaction(user, game):
    try:
        action = UserGameAction.objects.get(game=game, user=user)
    except UserGameAction.DoesNotExist:
        return None
    return action.action