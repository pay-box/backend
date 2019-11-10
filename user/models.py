from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.files.base import ContentFile
from colorfield.fields import ColorField
import base64
from pay.settings import MEDIA_ROOT
from django.db.models import Q
from .constants import PERMISSIONS, USER_TYPES, DEVICE_TYPES
from django.core.files.storage import default_storage
# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=100, choices=USER_TYPES)
    permissions = ArrayField(
        models.CharField(
            max_length=100,
            blank=True,
            choices=PERMISSIONS
        ),
        null=True,
        blank=True
    )

    @classmethod
    def find(cls, role_name):
        role = Role.objects.filter(name=role_name).first()
        return role

    def __str__(self):
        return self.name


class User(AbstractUser):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        unique=False
    )
    roles = models.ManyToManyField(
        Role,
        related_name='user_roles'
    )
    details = JSONField(blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True)
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

    @classmethod
    def find(cls,
             user_pk):
        user = None

        user = User.objects.filter(
            Q(Q(email=user_pk) & Q(email__isnull=False)) |
            Q(Q(phone_number=user_pk) & Q(phone_number__isnull=False))
        ).first()

        return user

    @classmethod
    def update(cls, user, data):
        if 'fullname' in data:
            user.fullname = data['fullname']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'nickname' in data:
            user.nickname = data['nickname']
        if 'avatar' in data and data['avatar'] and \
                data['avatar'].find("http") != 0:
            user.avatar.save(
                '%s.jpg' % (user.username),
                ContentFile(
                    base64.b64decode(data['avatar'])
                ), save=True
            )

        if 'details' in data:
            if user.details is None:
                user.details = {}
            for key in data['details']:
                if isinstance(key, str) and key.endswith('_photo') and \
                        data['details'][key] and \
                        data['details'][key].find('http') != 0:
                    # Save the photo in a file and save the file path in db
                    _file = ContentFile(base64.b64decode(data['details'][key]))
                    _path = '%s/user_details/%s_%s.jpg' % \
                            (MEDIA_ROOT, key, user.username)
                    url = '{media_url}user_details/%s_%s.jpg' % \
                          (key, user.username)
                    if default_storage.exists(_path):
                        default_storage.delete(_path)
                    default_storage.save(_path, _file)
                    user.details[key] = url
                else:
                    user.details[key] = data['details'][key]

        if 'first_name' in data or 'last_name' in data:
            user.fullname = user.first_name
            if user.last_name:
                user.fullname += " " + user.last_name
        # try:
        #     # update_messenger_account(user)
        # except Exception:
        #     pass
        user.save()
        return user

    def __str__(self):
        return self.phone_number or self.username or ''


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
    title = models.CharField(max_length=300, null=True, blank=True)
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
        return self.title or "Config"

    @classmethod
    def get(self):
        return Config.objects.order_by('-modified_at').first()


class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='device_user'
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
    def find(cls, device_id):
        return Device.objects.filter(
            device_id=device_id
        ).first()

    @classmethod
    def add(cls, device_id, token, type, user):
        device = Device(
            user=user,
            device_id=device_id,
            token=token,
            type=type,
        )
        device.save()
        return device

    @classmethod
    def delete_device(cls, device_id):
        Device.objects.filter(
            device_id=device_id
        ).delete()
        return True

    def __str__(self):
        return '%s\'s %s' % (
            self.user.phone_number,
            self.type
        )
