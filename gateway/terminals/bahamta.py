from gateway.terminals.base import BaseTerminal
import requests
from django.conf import settings
from rest_framework.exceptions import APIException

MAKE_REQUEST_URL = "https://webpay.bahamta.com/api/create"\
                    "_request?api_key=%s&reference=%s&amount_irr"\
                    "=%d&callback_url=%s"
CONFIRM_URL = "https://webpay.bahamta.com/api/confirm_payment"\
                "?api_key=%s&reference=%s&amount_irr=%d"

MAKE_REQUEST_URL_DEBUG = "https://testwebpay.bahamta.com/api/create"\
                    "_request?api_key=%s&reference=%s&amount_irr"\
                    "=%d&callback_url=%s"
CONFIRM_URL_DEBUG = "https://testwebpay.bahamta.com/api/confirm_payment"\
                "?api_key=%s&reference=%s&amount_irr=%d"

MIN_PAYMENT_AMOUNT = 10000
MAX_PAYMENT_AMOUNT = 500000000


class BahamtaTerminal(BaseTerminal):

    def make_request(self, ref_num, amount):
        try:
            url = MAKE_REQUEST_URL
            if 'debug' in self.gateway.details:
                url = MAKE_REQUEST_URL_DEBUG
            res = requests.get(
                url % (
                    self.gateway.details['api_key'],
                    ref_num,
                    amount,
                    '%s/transaction/callback/%s' % (
                        settings.BASE_URL,
                        ref_num
                    )
                )
            )
            return res.json()['result']['payment_url']
        except Exception as e:
            raise e
            raise APIException("Something went wrong")

    def confirm(self, ref_num, amount):
        try:
            url = CONFIRM_URL
            if 'debug' in self.gateway.details:
                url = CONFIRM_URL_DEBUG
            res = requests.get(
                url % (
                    self.gateway.details['api_key'],
                    ref_num,
                    amount,
                )
            )
            print("#################")
            print(res.json())
            return res.json()['result']['state'] == 'paid'
        except Exception as e:
            raise e
            return False
