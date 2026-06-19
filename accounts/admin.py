from django.contrib import admin
from django.contrib.auth import get_user_model
from unfold.admin import ModelAdmin

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_display_links = ['username']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    filter_horizontal = ['groups', 'user_permissions']
