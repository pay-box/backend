from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from gateway.models import Gateway
from user.models import User, Config
from transaction.models import Transaction
from django.core.cache import cache
from django.http import HttpResponseRedirect
from pay.decorators import app_has_permission
from django.utils.translation import ugettext_lazy as _
from pay.utils import (
    humanizeAmount,
    getJalaliDate,
    humanizeNumber,
    persianiser
)
import json
# Create your views here.


def get_payer_name(user):
    if user and user.fullname is not None:
        return user.fullname
    elif user and user.phone_number is not None:
        return persianiser(humanizeNumber(user.phone_number))
    else:
        return None


class TransactionItemView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Transaction"
        ],
        operation_summary='Get request Status',
        query_serializer=serializers.RequestTransactionViewGet
    )
    @app_has_permission()
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestTransactionViewGet(
            data=request.query_params
        )
        if serializer.is_valid():
            transaction = Transaction.get(
                serializer.validated_data['ref_num']
            )
            if transaction:
                return Response(
                    serializers.Transaction(
                        transaction,
                        many=False
                    ).data,
                    status.HTTP_200_OK
                )
            else:
                temp_transaction = cache.get("transaction:%s" % (
                        serializer.validated_data['ref_num']
                    )
                )
                transaction = None
                if temp_transaction is not None:
                    transaction = json.loads(temp_transaction)
                    if transaction['application'] == request.application.id:
                        if transaction['state'] == 'pay':
                            transaction['status'] = 'pending'
                            return Response(
                                transaction,
                                status=status.HTTP_200_OK
                            )
                return Response(
                    {
                        "message": "No transaction found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TransactionMakeView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Transaction"
        ],
        operation_summary='Make Request',
        query_serializer=serializers.RequestTransactionMakePost
    )
    @app_has_permission()
    def post(self, request, *args, **kwargs):
        serializer = serializers.RequestTransactionMakePost(
            data=request.data
        )
        if serializer.is_valid():
            currency = serializer.validated_data['currency']
            gateway_id = serializer.validated_data.get('gateway_id', None)
            gateways_query = Gateway.list(
                gateway_id,
                currency
            )
            if gateways_query.count() > 0:
                user = User.get_user(
                    phone_number=serializer.validated_data.get(
                        'phone_number',
                        None
                    ),
                    email=serializer.validated_data.get(
                        'email',
                        None
                    ),
                    username=serializer.validated_data.get(
                        'username',
                        None
                    ),
                )
                print(user)
                transaction = Transaction.make_request(
                    amount=serializer.validated_data.get('amount', None),
                    currency=serializer.validated_data['currency'],
                    note=serializer.validated_data.get('note', None),
                    user=user,
                    gateways=gateways_query,
                    application=request.application,
                    continue_url=serializer.validated_data.get(
                        'continue_url',
                        None
                    )
                )
                url = '%s/transaction/payment/%s' % (
                    settings.BASE_URL,
                    transaction['ref_num']
                )
                return Response(
                    {
                        'url': url,
                        'ref_num': transaction['ref_num']
                    },
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': 'No gateway found with requested parameters'
                    },
                    status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TransactionCallbackView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Transaction"
        ],
        operation_summary='Callback receiver',
        query_serializer=serializers.RequestTransactionCallbackGet
    )
    def get(self, request, ref_num, *args, **kwargs):
        serializer = serializers.RequestTransactionCallbackGet(
            data=request.query_params
        )
        if serializer.is_valid():
            temp_transaction = cache.get("transaction:%s" % (
                    ref_num
                )
            )
            transaction = None
            if temp_transaction is not None:
                transaction = json.loads(temp_transaction)
                context = transaction
                context['state'] = 'pay'
                if 'gateway' in transaction and transaction['gateway']:
                    gateway = Gateway.objects.filter(
                        id=transaction['gateway']
                    ).first()

                    if serializer.validated_data['state'] == 'error':
                        Transaction.add_to_db(
                            transaction,
                            ref_num,
                            gateway,
                            False,
                            details={
                                'error_key': serializer.validated_data.get(
                                    'error_key', 'unknown',
                                ),
                                'error_message': serializer.validated_data.get(
                                    'error_message', 'unknown',
                                )
                            }
                        )
                    else:
                        result = Transaction.confirm_request(
                            ref_num, gateway, transaction['amount']
                        )
                        if result is not None:
                            Transaction.add_to_db(
                                transaction,
                                ref_num,
                                gateway,
                                result
                            )
                    return redirect(
                        '/transaction/payment/%s' % (ref_num)
                    )
                else:
                    cache.delete("transaction:%s" % (
                            ref_num
                        )
                    )
                    return redirect(
                        '/transaction/payment/%s' % (ref_num)
                    )
            else:
                return redirect(
                    '/transaction/payment/%s' % (ref_num)
                )

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'POST', ])
def transaction_payment_view(request, ref_num):
    if request.method == "GET":
        context = {}
        config = Config.get()
        temp_transaction = cache.get("transaction:%s" % (
                ref_num
            )
        )
        url = '%s/transaction/payment/%s' % (
            settings.BASE_URL,
            ref_num
        )
        transaction = None
        if temp_transaction is not None:
            transaction = json.loads(temp_transaction)
            context = transaction
            context['state'] = 'pay'
            if 'url' in transaction and transaction['url']:
                return HttpResponseRedirect(transaction['url'])
            else:
                user = User.get_user(username=transaction['username'])
                payer = get_payer_name(user)
                gateway = None
                gateways = []
                if 'gateway' in transaction and transaction['gateway']:
                    gateway = Gateway.objects.filter(
                        id=transaction['gateway']
                    ).first()
                else:
                    gateways = Gateway.objects.filter(
                        currency=transaction['currency']
                    ).all()
                amount_str = None
                if transaction['amount']:
                    amount_str = humanizeAmount(transaction['amount'])
                context = {
                    'state': 'pay',
                    'amount': amount_str,
                    'amount_value': transaction['amount'],
                    'gateway': gateway,
                    'gateways': gateways,
                    'user': user,
                    'note': transaction.get('note', None),
                    'background_color': config.pay_background_color,
                    'url': url,
                    # 'form': transaction.form,
                    'currency': transaction['currency'].upper(),
                    'payer': payer,
                    'title': transaction['title'],
                    'logo': transaction['logo'],
                }
                return render(request, 'transaction/pay.html', context)
        else:
            transaction = Transaction.get(ref_num=ref_num)

        if transaction is None:
            context = {
                'state': 'not_found',
                'background_color': config.error_background_color,
            }
            return render(request, 'transaction/pay.html', context)
        # print(transaction)
        payer = get_payer_name(transaction.user)
        background_color = config.paid_background_color,
        if transaction.status == 'rejected':
            background_color = config.error_background_color,
        context = {
            'state': transaction.status,
            'amount': humanizeAmount(transaction.amount),
            'gateway': transaction.gateway,
            'user': transaction.user,
            'background_color': background_color[0],
            'form': transaction.form,
            'currency': transaction.currency.upper(),
            'trace_no': persianiser(
                '%s-%d' % (transaction.random, transaction.id)
            ),
            'url': url,
            'note': transaction.note,
            'date': getJalaliDate(transaction.created_at),
            'payer': payer,
        }
        if transaction.application:
            context['title'] = transaction.application.title
            if transaction.application.logo:
                context['logo'] = transaction.application.logo.url

        if transaction.form:
            context['title'] = transaction.form.title
            if transaction.form.logo:
                context['logo'] = transaction.form.logo.url

        if 'continue_url' in transaction.details:
            context['continue_url'] = transaction.details['continue_url']
        return render(request, 'transaction/pay.html', context)
    else:
        temp_transaction = cache.get("transaction:%s" % (
                ref_num
            )
        )
        url = '%s/transaction/payment/%s' % (
            settings.BASE_URL,
            ref_num
        )
        transaction = None
        config = Config.get()
        if temp_transaction is not None:
            transaction = json.loads(temp_transaction)
            amount = request.data.get('amount', None)
            gateway_id = request.data.get('gateway', None)
            user = User.get_user(username=transaction['username'])
            payer = get_payer_name(user)
            gateway = None
            gateways = []
            if 'gateway' in transaction and transaction['gateway']:
                gateway = Gateway.objects.filter(
                    id=transaction['gateway']
                ).first()
            else:
                gateways = Gateway.objects.filter(
                    currency=transaction['currency']
                ).all()
            amount_str = None
            if transaction['amount']:
                amount_str = humanizeAmount(transaction['amount'])
            context = {
                'state': 'pay',
                'amount': amount_str,
                'amount_value': transaction['amount'],
                'gateway': gateway,
                'gateways': gateways,
                'background_color': config.pay_background_color,
                'note': transaction.get('note', None),
                'user': user,
                'url': url,
                # 'form': transaction.form,
                'currency': transaction['currency'].upper(),
                'payer': payer,
                'title': transaction['title'],
                'logo': transaction['logo'],
            }
            if amount is None or not amount:
                context['message'] = _('Please enter a valid amount.')
                return render(request, 'transaction/pay.html', context)
            if gateway_id is None:
                context['message'] = _('Please choose a gateway.')
                return render(request, 'transaction/pay.html', context)
            if int(amount) < settings.MIN_PAYMENT_AMOUNT:
                context['message'] = _(
                    'The minimum acceptable price is %(amount) %(currency)'
                ) % {
                    'amount': persianiser(
                        humanizeAmount(settings.MIN_PAYMENT_AMOUNT)
                    ),
                    'currency': transaction['currency'].upper()
                }
                return render(request, 'transaction/pay.html', context)
            if int(amount) > settings.MAX_PAYMENT_AMOUNT:
                context['message'] = _(
                    'The maximum acceptable price is %(amount) %(currency)'
                ) % {
                    'amount': persianiser(
                        humanizeAmount(settings.MAX_PAYMENT_AMOUNT)
                    ),
                    'currency': transaction['currency'].upper()
                }
                return render(request, 'transaction/pay.html', context)
            gateways_query = Gateway.list(
                gateway_id,
            )
            if amount:
                amount = int(amount)
            transaction = Transaction.update_request(
                        ref_num,
                        amount=amount,
                        gateways=gateways_query,
                    )
            if 'url' in transaction and transaction['url']:
                return HttpResponseRedirect(transaction['url'])
            else:
                url = '%s/transaction/payment/%s' % (
                    settings.BASE_URL,
                    ref_num
                )
                return HttpResponseRedirect(url)
        else:
            context = {
                'state': 'not_found',
                'background_color': config.error_background_color,
            }
            return render(request, 'transaction/pay.html', context)
