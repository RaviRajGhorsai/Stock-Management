from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AdminUser 


@admin.register(AdminUser)
class UserAdmin(BaseUserAdmin):
    model = AdminUser

    # Columns shown in the user list
    list_display = ('username', 'email', 'role', 'tenant', 'phone', 'sales_on', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')

    # Fields for editing existing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'role', 'tenant', 'sales_on')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'organization_name',
                'email',
                'organization_registration_number',
                'phone',
                'address',
                'active_duration',
                'sales_on',
                'role',
                'logo_image',
                'password1',
                'password2',
            ),
        }),
    )

    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
