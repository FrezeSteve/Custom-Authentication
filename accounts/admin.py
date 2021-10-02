from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, DeviceTracker


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_created')
    list_filter = ('staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_created')}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'last_name', 'device')}),
        ('Permissions', {'fields': ('admin', 'active', 'staff', 'is_superuser', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('date_created',)
    filter_horizontal = ()
    readonly_fields = ('date_created', "device")


# if settings.DEBUG:
#     class AnonymousUserAdmin(admin.ModelAdmin):
#         list_display = ('session_id', 'date_created')
# else:
#     class AnonymousUserAdmin(admin.ModelAdmin):
#         list_display = ('session_id', 'date_created')  #
#         readonly_fields = ('session_id', 'date_created', 'last_used')
class AnonymousUserAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'date_created')
    readonly_fields = ('date_created', 'last_used')


admin.site.register(User, UserAdmin)
admin.site.register(DeviceTracker, AnonymousUserAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
