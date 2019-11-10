from rest_framework import serializers

from pay.settings import MEDIA_URL
from .models import (
    User,
    Config,
)


class RequestUserAuthPost(serializers.Serializer):
    user_pk = serializers.CharField(required=True)


class RequestUserAuthPut(serializers.Serializer):
    user_pk = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class RequestUserItemGet(serializers.Serializer):
    username = serializers.CharField(required=True)


class ResponseUserEditPut(serializers.Serializer):
    fullname = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    details = serializers.SerializerMethodField(method_name='get_details',
                                                required=False)

    def get_details(self, user):
        if user.details is not None:
            for key in user.details:
                if isinstance(key, str) and key.endswith('_photo'):
                    user.details[key] = \
                        user.details[key].format(media_url=MEDIA_URL)
            return user.details
        return {}


class RequestUserEditPut(serializers.Serializer):
    fullname = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    details = serializers.JSONField(required=False)


class RequestAddDevicePost(serializers.Serializer):
    device_id = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    type = serializers.ChoiceField(required=True, choices=[
        'web',
        'android',
        'ios'
    ])


class ResponseProfile(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(method_name='get_details')

    def get_details(self, user):
        if user.details is not None:
            for key in user.details:
                if isinstance(key, str) and key.endswith('_photo'):
                    user.details[key] = \
                        user.details[key].format(media_url=MEDIA_URL)
            return user.details
        return {}

    class Meta:
        model = User
        exclude = [
            'user_permissions',
            'password',
            'is_staff',
            'groups',
            'is_superuser',
            "is_active",
            "roles"
        ]


class ResponseGroupMember(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'phone_number',
            'avatar',
            'username'
        ]


class ResponseUserDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'phone_number',
            'avatar',
            'username'
        ]


class ResponseUserConfig(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"
