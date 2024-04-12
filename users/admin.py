from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active')

    def activate_user(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)

    actions = ['deactivate_user']
    deactivate_user.short_description = "Disable user(s)"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
