from django.db import models
from django.contrib.postgres.fields import JSONField
from form.models import Form
from gateway.models import Gateway
from user.models import User, Application
from pay.constants import CURRENCY_TYPES
from pay.utils import generate_unique_id, generate_random
import json
from django.conf import settings
from django.core.cache import cache
from gateway.terminals.bahamta import BahamtaTerminal
# Create your models here.

STATUS_TYPES = (
    ('paid', 'Paid'),
    ('rejected', 'Rejected'),
)


class Transaction(models.Model):
    ref_num = models.CharField(max_length=100)
    res_num = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_TYPES)
    note = models.CharField(max_length=300)
    random = models.CharField(max_length=6, default=generate_random)
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="transaction_form",
        null=True, blank=True
    )
    gateway = models.ForeignKey(
        Gateway,
        on_delete=models.CASCADE,
        related_name="transaction_gateway",
        null=True, blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_user",
        null=True, blank=True
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="transaction_application",
        null=True, blank=True
    )
    currency = models.CharField(
        null=False,
        blank=False,
        max_length=5,
        default="irr",
        choices=CURRENCY_TYPES
    )
    amount = models.IntegerField()
    wage = models.IntegerField(default=0)

    details = JSONField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def get(cls, ref_num, application=None):
        query = Transaction.objects.filter(
           ref_num=ref_num
        )
        if application:
            query = query.filter(application=application)
        return query.first()

    @classmethod
    def add_to_db(cls, data, ref_num, gateway, success, details={}):
        transaction = Transaction.objects.filter(ref_num=ref_num).first()
        if transaction:
            raise ValueError("Transaction is already exists")
        user = User.objects.filter(username=data['username']).first()
        application = None
        form = None
        if 'application' in data:
            application = Application.objects.filter(
                id=data['application']
            ).first()
        if 'form' in data:
            form = Form.objects.filter(
                id=data['form']
            ).first()
        form = None
        if 'form' in data and data['form']:
            form = Form.objects.filter(id=data['form']).first()
        status = 'paid'
        for item in ['continue_url', ]:
            if item in data and data[item]:
                details[item] = data[item]
        if success is False:
            status = 'rejected'
        transaction = Transaction(
            amount=data['amount'],
            currency=data['currency'],
            form=form,
            user=user,
            details=details,
            application=application,
            gateway=gateway,
            res_num=ref_num,
            ref_num=ref_num,
            status=status
        )
        transaction.save()
        cache.delete("transaction:%s" % ref_num)

    @classmethod
    def update_request(cls, ref_num, amount, gateways):

        transaction = cache.get(
            "transaction:%s" % ref_num,
        )
        if transaction:
            transaction = json.loads(transaction)
        if gateways.count() == 1 and amount:
            gateway = gateways.first()
            transaction['gateway'] = gateway.id
            transaction['amount'] = amount
            if gateway.type == 'bahamta':
                bahamtaTerminal = BahamtaTerminal(gateway)
                url = bahamtaTerminal.make_request(ref_num, amount)
        if url is not None:
            transaction['url'] = url

        cache.set(
            "transaction:%s" % ref_num,
            json.dumps(transaction),
            timeout=settings.CACHE_TEMP_TRANSACTION_TTL
        )

        return transaction

    @classmethod
    def make_request(
            cls,
            amount,
            currency,
            user,
            gateways,
            application,
            continue_url,
            form=None):
        ref_num = generate_unique_id()
        url = None
        gateway = None
        if gateways.count() == 1 and amount:
            gateway = gateways.first()
            if gateway.type == 'bahamta':
                bahamtaTerminal = BahamtaTerminal(gateway)
                url = bahamtaTerminal.make_request(ref_num, amount)
        transaction = {
            'ref_num': ref_num,
            'amount': amount,
            'currency': currency,
            'username': user.username,
        }
        if gateway:
            transaction['gateway'] = gateway.id,
            try:
                transaction['gateway'] = transaction['gateway'][0]
            except Exception:
                pass
        if form:
            transaction['form'] = form.id
            transaction['title'] = form.title
            if form.logo:
                transaction['logo'] = form.logo.url
        if application:
            transaction['application'] = application.id,
            transaction['title'] = application.title
            if application.logo:
                transaction['logo'] = application.logo.url
        if continue_url:
            transaction['continue_url'] = continue_url
        if url is not None:
            transaction['url'] = url

        cache.set(
            "transaction:%s" % ref_num,
            json.dumps(transaction),
            timeout=settings.CACHE_TEMP_TRANSACTION_TTL
        )
        return transaction

    @classmethod
    def confirm_request(cls, ref_num, gateway, amount):
        if gateway.type == 'bahamta':
            bahamtaTerminal = BahamtaTerminal(gateway)
            result = bahamtaTerminal.confirm(ref_num, amount)
            return result
        else:
            return None
