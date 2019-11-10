from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        'auth',
        views.UserAuthView.as_view(),
        name='user_auth'
    ),
    url(
        'profile',
        views.UserProfileView.as_view(),
        name='user_profile'
    ),
    url(
        'device',
        views.UserDeviceView.as_view(),
        name='user_device'
    ),
]
