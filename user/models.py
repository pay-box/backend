from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
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
        if username is not None:
            user = User.objects.filter(username=username).first()
        else:
            username = uuid.uuid4().hex.replace('-', '')

        if user:
            return user

        user = User(
            username=username,
            phone_number=phone_number,
            email=email,
            fullname=fullname
        )
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
