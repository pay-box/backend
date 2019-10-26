from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings
from form.models import Form
from gateway.models import Gateway
from transaction.models import Transaction
from user.models import User
from pay.utils import (
    humanizeAmount,
)
from django.http import HttpResponseRedirect


@api_view(['GET', 'POST', ])
def form_form_view(request, id, random):
    if request.method == "GET":
        context = {}
        form = Form.get(id, random)
        if form:
            url = '%s/form/%s/%s' % (
                settings.BASE_URL,
                form.id,
                form.random
            )
            gateway = None
            gateways = []
            amount_str = None
            if form.amount:
                amount_str = humanizeAmount(form.amount)
            gateway = None
            if form.gateways.count() == 1:
                gateway = form.gateways.first()
                gateways = []
            elif form.gateways.count() > 1:
                gateways = form.gateways.all()
            else:
                context = {
                    'state': 'not_found',
                    'error': 'در حال حاضر امکان پرداخت در'
                             ' این درگاه وجود ندارد.'
                }
                return render(request, 'transaction/pay.html', context)
            context = {
                'state': 'pay',
                'amount': amount_str,
                'amount_value': form.amount,
                'gateway': gateway,
                'gateways': gateways,
                'url': url,
                # 'form': transaction.form,
                'currency': form.currency,
                'title': form.title,
                'logo': form.logo.url,
                'background_color': form.background_color,
                'text_color': form.text_color,
                'note_mode': form.note_mode
            }
            return render(request, 'transaction/pay.html', context)

    else:
        pass
        amount = request.data.get('amount', None)
        gateway_id = request.data.get('gateway', None)
        gateways_query = Gateway.list(
            gateway_id,
        )
        username = None
        if 'username' in request.data:
            username = request.data['username']
        user = User.get_user(
            phone_number=None,
            email=None,
            username=username
        )
        form = Form.get(id, random)
        if amount:
            amount = int(amount)
        transaction = Transaction.make_request(
                    currency=form.currency,
                    amount=amount,
                    application=None,
                    user=user,
                    continue_url=None,
                    gateways=gateways_query,
                    form=form
                )
        if 'url' in transaction and transaction['url']:
            return HttpResponseRedirect(transaction['url'])
        else:
            url = '%s/transaction/payment/%s' % (
                settings.BASE_URL,
                transaction['ref_num']
            )
            return HttpResponseRedirect(url)


@api_view(['GET', ])
def form_list_view(request):
    if request.method == "GET":
        forms = Form.list()
        for form in forms:
            form.gateway = None
            if form.gateways.count() == 1:
                form.gateway = form.gateways.first()
        return render(request, 'form.html', {
            'forms': forms
        })
