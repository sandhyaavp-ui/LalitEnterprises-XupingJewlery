from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'read_minutes')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
