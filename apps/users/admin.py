from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'id',
        'email',
        'is_verified',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'is_verified',
    )
    raw_id_fields = ('groups', 'user_permissions')
    readonly_fields = ['date_joined']
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    readonly_fields = ["date_joined"]
    
    actions = ["make_published"]

    @admin.action(description="Make selected users verified")
    def make_verified(self, request, queryset):
        queryset.update(is_verified=True)
    
