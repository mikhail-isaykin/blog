from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Profile
from unfold.admin import ModelAdmin

User = get_user_model()

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['pk', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_display_links = ['username']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    filter_horizontal = ['groups', 'user_permissions']


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ['permissions']


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'bio']
    list_display_links = ['user']
    search_fields = ['user__username', 'bio']
    raw_id_fields = ['user']
