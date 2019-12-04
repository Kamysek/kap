from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.forms import CustomUserCreationForm, CustomUserChangeForm
from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'email_notification')
    list_filter = ('username', 'email', 'is_staff', 'is_active', 'email_notification')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('groups', 'is_staff', 'is_active', 'email_notification')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'groups', 'is_staff', 'is_active', 'email_notification')}
         ),
    )
    search_fields = ('username', 'email', 'email_notification')
    ordering = ('username', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)
