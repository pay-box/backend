from django.db import models
from gateway.models import Gateway
from pay.constants import CURRENCY_TYPES
from colorfield.fields import ColorField
from pay.utils import generate_random
# Create your models here.

NOTE_TYPES = (
    ('disabled', 'Disabled'),
    ('optional', 'Optional'),
    ('required', 'Required'),
)


class Form(models.Model):
    title = models.CharField(max_length=300)
    gateways = models.ManyToManyField(
        Gateway,
        related_name="form_gateway",
        blank=True
    )
    amount = models.IntegerField(null=True, blank=True)
    random = models.CharField(max_length=6, default=generate_random)
    logo = models.ImageField(null=True, blank=True)
    background_color = ColorField(default='#327F8F')
    text_color = ColorField(default='#FFFFFF')
    description = models.CharField(max_length=300, null=True, blank=True)
    note_mode = models.CharField(
        max_length=20,
        default='disabled',
        choices=NOTE_TYPES
    )
    currency = models.CharField(
        null=False,
        blank=False,
        max_length=5,
        default="irr",
        choices=CURRENCY_TYPES
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
    def get(cls, id, random=None):
        query = Form.objects.filter(id=id)
        if random:
            query = query.filter(random=random)
        return query.first()

    @classmethod
    def list(cls):
        return Form.objects.all()
