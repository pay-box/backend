from pay.celery import app as celery_app
from .kavenegar import KavenegarSMS
from django.conf import settings
from django.template.loader import render_to_string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib


def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)


@celery_app.task(name='send_verify')
def send_verify(user_pk, code, email=False):
    if not settings.TESTING:
        if not email:
            kavenegar = KavenegarSMS()
            kavenegar.verify(
                user_pk,
                code
            )
        else:
            send_email(
                user_pk,
                code,
                "activation_code"
            )


@celery_app.task(name='send_email')
def send_email(email, code, template, locale_prefix=''):
    message = render_to_string(
        "user/{}.html".format(locale_prefix + template),
        {
            "header": settings.EMAIL_TEMPLATE[
                locale_prefix + template]["header"],
            "content": settings.EMAIL_TEMPLATE[
                locale_prefix + template]["content"],
            "code": code,
            "icon": settings.EMAIL_TEMPLATE[locale_prefix + template]["icon"],
            "logo_url": settings.BASE_URL + "/static/images/logo.png"
        }
    )
    msg = MIMEMultipart('alternative')
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = "Email Verification"
    if contains_non_ascii_characters(message):
        html_text = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
    else:
        html_text = MIMEText(message, 'html')

    if(contains_non_ascii_characters(message)):
        plain_text = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')
    else:
        plain_text = MIMEText(message, 'plain')
    msg.attach(plain_text)
    msg.attach(html_text)
    msg['Content-Type'] = "text/html; charset=utf-8"
    s = smtplib.SMTP_SSL(settings.EMAIL_SERVER, 465)

    s.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
    s.sendmail(settings.EMAIL_FROM, email, msg.as_string())
    s.quit()
