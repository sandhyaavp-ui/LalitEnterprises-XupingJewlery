from django.contrib import admin
from .models import BlogPost, Testimonial


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'read_minutes')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'approved', 'submitted_at')
    list_filter = ('approved', 'rating')
    search_fields = ('name', 'message')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(approved=True)
    approve_selected.short_description = "Approve selected reviews"
