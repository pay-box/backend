from django.contrib import admin
from user.models import Application, User, Config
# Register your models here.

admin.site.register(Application)
admin.site.register(User)
admin.site.register(Config)
