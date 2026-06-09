from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'created']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
