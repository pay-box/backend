from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from colorfield.fields import ColorField
from django.db.models import Q
# Create your models here.


class User(AbstractUser):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        unique=False
    )
    email = models.EmailField(_('email address'), null=True, blank=True)
    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def get_user(cls,
                 email=None,
                 phone_number=None,
                 username=None,
                 fullname=None):
        user = None
        if username is None:
            username = uuid.uuid4().hex.replace('-', '')

        user = User.objects.filter(
            Q(Q(email=email) & Q(email__isnull=False)) |
            Q(Q(phone_number=phone_number) & Q(phone_number__isnull=False)) |
            Q(Q(username=username) & Q(username__isnull=False))
        ).first()
        if user:
            return user

        user = User(
            username=username,
            phone_number=phone_number,
            email=email,
            fullname=fullname
        )
        user.save()
        return user


class Application(models.Model):
    title = models.CharField(max_length=300)
    token = models.CharField(max_length=300)
    logo = models.ImageField(null=True, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="application_owner",
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


class Config(models.Model):
    title = models.CharField(max_length=300)
    logo = models.ImageField(null=True, blank=True)
    background_color = ColorField(default='#327F8F')
    paid_background_color = ColorField(default='#45c175')
    pay_background_color = ColorField(default='#4585c1')
    error_background_color = ColorField(default='#808080')
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
