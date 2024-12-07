from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("id", "username", "email", "is_staff", "is_active")

    readonly_fields = ("id",)

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("id",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("id",)}),)
