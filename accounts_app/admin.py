from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from accounts_app.models import CustomUser
from accounts_app.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["email", "full_name", "personal_number", "is_staff", "role"]
    list_filter = ["is_staff", "is_active", "role", "groups"]

    fieldsets = (
        ("Account Information", {
            "fields": (("email", "password"),),
            "classes": ("wide",),
            "description": "User Details"
        }),
        ("Personal Info", {
            "fields": (("full_name",), ("personal_number", "birth_date"), "date_joined"),
            "classes": ("collapse",),
            "description": "Personal Information"
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "role", "groups", "user_permissions"),
            "classes": ("collapse",),
            "description": "User Permissions"
        }),
        ("Important Dates", {
            "fields": ("last_login",),
            "classes": ("collapse",),
            "description": "Important dates related to the user"
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2', 'is_staff', 'is_active',
            'role', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ["email", "full_name", "personal_number"]
    ordering = ["email"]
    filter_horizontal = ["groups", "user_permissions"]
