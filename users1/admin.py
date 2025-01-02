from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users1.models.user_model import User
from users1.models.status_model import Status
from users1.models.base_model import BaseModel,GenericBaseModel

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    readonly_fields = ('created_at', 'updated_at')

