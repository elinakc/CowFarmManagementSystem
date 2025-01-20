from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.Users_app.models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('-date_joined',)
    list_display = ('username', 'email', 'roles', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields':('username', 'email','password',)}),
        ('Personal info',{'fields':('roles','phone_number','address',)}),
        ('Permissions',{'fields':('is_staff','is_superuser',)}),
        ('Important dates',{'fields':('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes':('wide',),
        'fields':('username','password1', 'password2','email','roles','phone_number','address'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
