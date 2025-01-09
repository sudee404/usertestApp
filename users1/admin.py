from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError
from django.contrib import messages
from users1.models.user_model import User
from users1.models.status_model import Status


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active', 'created_at', 'updated_at', 'PROFILE_LOGO')
    list_filter = ('is_active', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'PROFILE_LOGO')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'PROFILE_LOGO'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    # Override save_model to handle foreign key integrity issues
    def save_model(self, request, obj, form, change):
        try:
            # Attempt to save the object
            super().save_model(request, obj, form, change)
        except IntegrityError as e:
            # Log the error and notify the user
            messages.error(request, f"Error saving user: {str(e)}")
            raise

    # Override delete_model to handle foreign key integrity issues during deletion
    def delete_model(self, request, obj):
        try:
            obj.delete()
        except IntegrityError as e:
            messages.error(request, f"Error deleting user: {str(e)}")
            raise


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')
