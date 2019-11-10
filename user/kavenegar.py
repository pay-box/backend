import requests
from django.conf import settings


class KavenegarSMS:
    BASE_URL = 'http://api.kavenegar.com/v1/%s' % settings.KAVENEGAR_API_KEY

    def send_sms(self, receptor, message, sender=settings.KAVENEGAR_NUMBER):
        url = '%s/sms/send.json' % self.BASE_URL
        reponse = requests.post(
            url=url,
            verify=False,
            data={
                'receptor': receptor,
                'message': message,
            },
        )
        return reponse

    def verify(self, receptor, code):
        url = '%s/sms/send.json' % self.BASE_URL
        reponse = requests.post(
            url=url,
            verify=False,
            data={
                'receptor': receptor,
                'message': "کد فعال سازی شما: %s" % (code),
                'sender': settings.KAVENEGAR_NUMBER,
            },
        )
        return reponse

    def lookup(self, receptor, template, token, token2=None, token3=None):
        url = '%s/verify/lookup.json' % self.BASE_URL
        data = {
            'receptor': receptor,
            'template': template,
            'token': token,
        }
        if token2 is not None:
            data['token2'] = token2
        if token3 is not None:
            data['token3'] = token3
        response = requests.post(
            url=url,
            verify=False,
            data=data,
        )
        return response

    def select(self, messageid):
        url = '%s/sms/select.json' % self.BASE_URL
        data = {
            'messageid': messageid,
        }
        response = requests.post(
            url=url,
            verify=False,
            data=data,
        )
        return response
