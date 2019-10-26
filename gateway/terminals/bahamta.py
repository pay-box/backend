from gateway.terminals.base import BaseTerminal
import requests
from django.conf import settings
from rest_framework.exceptions import APIException

MAKE_REQUEST_URL = "https://webpay.bahamta.com/api/create"\
                    "_request?api_key=%s&reference=%s&amount_irr"\
                    "=%d&callback_url=%s"
CONFIRM_URL = "https://webpay.bahamta.com/api/confirm_payment"\
                "?api_key=%s&reference=%s&amount_irr=%d"


class BahamtaTerminal(BaseTerminal):

    def make_request(self, ref_num, amount):
        try:
            res = requests.get(
                MAKE_REQUEST_URL % (
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
            res = requests.get(
                CONFIRM_URL % (
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
