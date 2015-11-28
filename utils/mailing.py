# coding=utf-8
from django.core.mail import send_mail as django_send_email
from django.template.loader import render_to_string
from sportcourts import settings


def send_email(email, subject, content, plain_content=''):
    return django_send_email(subject, plain_content, settings.EMAIL_HOST_USER, [email], html_message=content,
                             fail_silently=True)


def verify_email(email, token):
    body = render_to_string('mail/email_verify.html', {'token': token, 'current_host': settings.CURRENT_HOST})
    return send_email(email, u'Подтверждение адреса электронной почты', body)