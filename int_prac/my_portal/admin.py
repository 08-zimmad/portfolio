from django.contrib import admin

from my_portal import models

# Register your models here.


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "email", "user_type", "is_staff")
    list_filter = ("username", "is_staff")
    search_field = ("username", "email")
