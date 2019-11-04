from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        '^make',
        views.TransactionMakeView.as_view(),
        name='transaction_make'
    ),
    url(
        '^item',
        views.TransactionItemView.as_view(),
        name='transaction_item'
    ),
    url(
        r'^callback/(?P<ref_num>\w{0,50})',
        views.TransactionCallbackView.as_view(),
        name='transaction_payment'
    ),
    url(
        r'^payment/(?P<ref_num>\w{0,50})',
        views.transaction_payment_view,
        name='transaction_payment'
    ),

]
