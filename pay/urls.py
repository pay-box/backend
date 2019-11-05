"""pay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from user import views as user_views
from form import views as form_views

schema_view = get_schema_view(
   openapi.Info(
      title="Open Pay API",
      default_version='v1',
      description="Make payment great again!",
      terms_of_service="https://open-pay.ir/terms/",
      contact=openapi.Contact(email="info@open-pay.ir"),
      license=openapi.License(name="BSD License"),
      url="https://open-pay.ir/api"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', user_views.intro, name='index'),
    path('forms', form_views.form_list_view, name='index'),
    path('admin/', admin.site.urls),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    # path(r'user/', include('user.urls')),
    path(r'form/', include('form.urls')),
    # path(r'gateway/', include('gateway.urls')),
    path(r'transaction/', include('transaction.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += static(
    settings.MEDIA_RELATIVE_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += i18n_patterns(
    path('', user_views.intro, name='index'),
    path(r'form/', include('form.urls')),
    path(r'transaction/', include('transaction.urls')),
)
