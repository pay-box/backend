from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<id>\w{0,50})/(?P<random>\w{0,50})',
        views.form_form_view,
        name='form_form'
    ),
]
