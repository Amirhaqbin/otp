from django.contrib import admin
from .models import CostumeUser, OtpRequest
from django.contrib.auth.admin import UserAdmin

admin.site.register(OtpRequest)

@admin.register(CostumeUser)
class AppUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff")
