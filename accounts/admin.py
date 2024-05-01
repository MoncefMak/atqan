from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Permissions',
         {'fields': ('is_superuser', 'is_managed', 'is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = (
        'email', 'first_name', 'last_name', 'date_of_birth', 'is_superuser', 'is_managed', 'is_active', 'is_staff'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
