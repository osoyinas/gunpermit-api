from django.contrib import admin
from .models import CustomUser
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ["id", "username", "email", "auth_provider", "is_active", "is_staff", "date_joined"]
    list_filter = ["is_active", "is_staff", "auth_provider", "date_joined"]
    search_fields = ["username", "email", "id"]


admin.site.register(CustomUser, UserAdmin)
