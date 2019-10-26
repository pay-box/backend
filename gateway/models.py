from django.db import models
from django.contrib.postgres.fields import JSONField
from pay.constants import CURRENCY_TYPES
from gateway.constants import GATEWAY_TYPES
# Create your models here.


class Gateway(models.Model):
    title = models.CharField(max_length=300)
    currency = models.CharField(
        null=False,
        blank=False,
        max_length=5,
        default="irr",
        choices=CURRENCY_TYPES
    )
    type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=GATEWAY_TYPES
    )
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

    def __str__(self):
        return self.title

    @classmethod
    def get(cls, gateway_id):
        return Gateway.objects.filter(id=gateway_id).first

    @classmethod
    def list(cls, gateway_id=None, currency=None):
        query = Gateway.objects
        if gateway_id is not None:
            query = query.filter(id=gateway_id)
        if currency is not None:
            query = query.filter(currency=currency)
        return query
