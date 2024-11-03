from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "auth_provider", "date_joined"]


admin.site.register(CustomUser, UserAdmin)
