from rest_framework.exceptions import MethodNotAllowed


class BaseTerminal:
    def __init__(self, gateway):
        self.gateway = gateway

    def make_request(self, ref_num, amount):
        raise MethodNotAllowed(
            "This method is not implemented in this gateway"
        )

    def confirm(self, ref_num, amount):
        raise MethodNotAllowed(
            "This method is not implemented in this gateway"
        )
