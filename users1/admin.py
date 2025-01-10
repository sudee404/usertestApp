# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.db import IntegrityError, transaction
from users1.models.user_model import User
from users1.models.status_model import Status
from django.contrib.auth.models import Group

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "is_active", "is_staff", "created_at", "updated_at", "profile_logo")
    list_filter = ("is_active", "is_staff", "created_at", "updated_at")
    search_fields = ("email", "username")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "profile_logo")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "profile_logo"),
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle saving users with validation for related groups and permissions.
        """
        try:
            with transaction.atomic():
                # Validate group existence only if changing an existing user
                if change:
                    for group in obj.groups.all():
                        if not Group.objects.filter(id=group.id).exists():
                            raise IntegrityError(f"Group with ID {group.id} does not exist.")
                
                # Save the user instance
                super().save_model(request, obj, form, change)
                messages.success(request, f"User '{obj.email}' saved successfully.")
        except IntegrityError as e:
            messages.error(request, f"Error saving user: {str(e)}")
            raise

    def delete_model(self, request, obj):
        """
        Override delete_model to handle user deletion with proper error messages.
        """
        try:
            obj.delete()
            messages.success(request, f"User '{obj.email}' deleted successfully.")
        except IntegrityError as e:
            messages.error(request, f"Error deleting user: {str(e)}")
            raise

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Status model.
    """
    list_display = ("name", "description", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)