from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['userid']
    list_display = ['userid', 'firstname', 'middlename', 'lastname',
                    'phonenumber', 'emailid', 'dob', 'gender',
                    'firebaseuserid']
    fieldsets = (
        (None, {'fields': ('firebaseuserid',)}),
        (_('Personal Info'), {'fields': ('firstname', 'middlename', 'lastname',
                              'phonenumber', 'emailid', 'dob', 'gender')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firebaseuserid',)
        }),
    )


admin.site.register(models.User, UserAdmin)
# admin.site.register(models.Event)
