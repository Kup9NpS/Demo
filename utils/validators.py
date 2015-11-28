# coding=utf-8
from django.core.exceptions import ValidationError
from utils.datetimehelps import DateTime


def validate_password(value):
    if len(value) < 4:
        raise ValidationError('Пароль слишком уж короткий!')
    if not all(map(lambda x: 97 <= ord(x) <= 122 or x.isdigit(), value.lower())):
        raise ValidationError('Только латинские буквы или цифры.')


def gte_now(d):
    error = ValidationError('Нельзя добавить в прошлое.')
    if d < DateTime.now():
        raise error


def validate_height(value):
    if value != 0 and (value > 250 or value < 100):
        raise ValidationError('Твой рост {}. Серьезно?'.format(value))


def validate_weight(value):
    if value != 0 and (value > 200 or value < 20):
        raise ValidationError('Твой вес {}. Серьезно?'.format(value))