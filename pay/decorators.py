from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from user import models


User = get_user_model()


def app_has_permission():
    def decorator(function):
        def wrapper(*args, **kwargs):
            request = args[1]

            # check for organization authentication
            if "HTTP_ACCESS_TOKEN" not in request.META or \
                    not request.META["HTTP_ACCESS_TOKEN"]:
                return Response(
                    {"message": "ACCESS-TOKEN header not provided."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            token = request.META["HTTP_ACCESS_TOKEN"]
            application = models.Application.objects.filter(
                token=token,
                active=True,
            ).first()
            # TODO: check permission
            if not application:
                return Response(
                    {"message": "شما اجازه این کار را ندارید."},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                request.application = application

            return function(*args, **kwargs)

        return wrapper

    return decorator
