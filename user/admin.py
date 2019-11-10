from django.contrib import admin
from user.models import Application, User, Config, Role
# Register your models here.

admin.site.register(Application)
admin.site.register(Config)
admin.site.register(Role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'fullname', 'username']
    list_display = [
        "id",
        "phone_number",
        "fullname",
        "username"
    ]

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()
