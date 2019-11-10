from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from pay.decorators import has_permission
from . import serializers
from . import tasks
from user.utils import generate_random_code
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from user.models import User, Device
from rest_framework import status
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


@api_view(['GET', ])
def intro(request):
    return render(request, 'intro.html', {
    })


class UserAuthView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "User"
        ],
        operation_summary='Login',
        query_serializer=serializers.RequestUserAuthPost
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.RequestUserAuthPost(
            data=request.data
        )
        if serializer.is_valid():
            user = User.find(
                user_pk=serializer.validated_data['user_pk']
            )

            if not user:
                return Response({
                        'message': _("No user found with this parameters.")
                    },
                    status.HTTP_404_NOT_FOUND
                )

            login_counter = cache.get("user:%s:confirm:counter" % (
                serializer.validated_data['user_pk']
            ))
            if login_counter is None or login_counter == '':
                login_counter = 0
            if int(login_counter) > settings.VERIFY_CODE_LOCK_LIMIT:
                return Response({
                    'message': _("Too much wrong attemps."
                                " Please try in 24 later.")
                },
                    status.HTTP_403_FORBIDDEN)
            cache.set("user:%s:confirm:counter" % (
                serializer.validated_data['user_pk']
            ),
                      login_counter + 1,
                      timeout=settings.VERIFY_CODE_LOCK_TTL
                      )
            verify_code = generate_random_code(6)
            if not settings.TESTING:
                tasks.send_verify.delay(
                    serializer.validated_data['user_pk'],
                    verify_code,
                    serializer.validated_data['user_pk'] == user.email
                )
            cache.set("user:%s:confirm" % (
                serializer.validated_data['user_pk']
            ),
                      verify_code,
                      timeout=settings.VERIFY_CODE_TTL
                      )
            return Response({
            },
                status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Cofirm Login',
        query_serializer=serializers.RequestUserAuthPut
    )
    def put(self, request, *args, **kwargs):
        serializer = serializers.RequestUserAuthPut(
            data=request.data
        )
        if serializer.is_valid():
            user = User.find(
                user_pk=serializer.validated_data['user_pk']
            )
            if not user:
                return Response(
                    {
                        "message": "Phone number not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            verify_code = cache.get("user:%s:confirm" % (
                serializer.validated_data['user_pk']
            )
                                    )

            if verify_code != serializer.validated_data['code']:
                return Response(
                    {
                        "message": _("The entered code is wrong.")
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            cache.delete("user:%s:confirm" % (
                serializer.validated_data['user_pk']
            )
                         )
            cache.delete("user:%s:confirm:counter" % (
                serializer.validated_data['user_pk']
            ))
            token, created = Token.objects.get_or_create(user=user)
            user_data = serializers.ResponseProfile(instance=user).data
            data = {
                'token': token.key,
                'user': user_data
            }

            return Response(data, status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Get Profile',
    )
    @has_permission('can_get_profile')
    def get(self, request, *args, **kwargs):
        return Response(serializers.ResponseProfile(request.user).data,
                        status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProfile(many=False)
        },
        tags=[
            "User"
        ],
        operation_summary='Edit Profile',
        query_serializer=serializers.RequestUserEditPut
    )
    @has_permission('can_edit_profile')
    def put(self, request, *args, **kwargs):
        serializer = serializers.RequestUserEditPut(
            data=request.data
        )
        if serializer.is_valid():
            user = User.update(request.user, serializer.validated_data)
            return Response(serializers.ResponseProfile(user).data,
                            status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDeviceView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "User"
        ],
        security=[],
        operation_summary='Add Device',
        query_serializer=serializers.RequestAddDevicePost
    )
    @has_permission('can_add_device')
    def post(self, request, version=1, user=None, *args, **kwargs):
        serializer = serializers.RequestAddDevicePost(
            data=request.data
        )
        if serializer.is_valid():
            device = Device.find(
                serializer.validated_data['device_id']
            )
            if device:
                device.device_id = serializer.validated_data['device_id']
                device.token = serializer.validated_data['token']
                device.save()
            else:
                device = Device.add(
                    serializer.validated_data['device_id'],
                    serializer.validated_data['token'],
                    serializer.validated_data['type'],
                    request.user
                )
            return Response(
                {
                    "success": True
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
