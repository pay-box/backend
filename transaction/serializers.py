from rest_framework import serializers
from pay.constants import CURRENCY_TYPES_LIST
from transaction.models import Transaction


class RequestTransactionMakePost(serializers.Serializer):
    amount = serializers.IntegerField(
        required=False,
        min_value=10000,
        max_value=500000000
    )
    gateway_id = serializers.IntegerField(required=False)
    phone_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    continue_url = serializers.CharField(required=False)
    currency = serializers.ChoiceField(
        required=True,
        choices=CURRENCY_TYPES_LIST
    )


class RequestTransactionViewGet(serializers.Serializer):
    ref_num = serializers.CharField(required=True)


class RequestTransactionCallbackGet(serializers.Serializer):
    reference = serializers.CharField(required=True)
    error_key = serializers.CharField(required=False)
    error_message = serializers.CharField(required=False)
    state = serializers.ChoiceField(
        required=True,
        choices=['wait_for_confirm', 'error']
    )


class ResponseTransaction(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
