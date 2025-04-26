from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "prenom", "nom", "profile_type", "is_staff")
    list_filter = ("profile_type",)
    search_fields = ("username", "prenom", "nom")
