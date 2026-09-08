from urllib.parse import quote

from django.contrib import admin
from django.utils.html import format_html

from .models import ContactSubmission, VideoCallBooking, Order, OrderItem


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'submitted_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('submitted_at',)


@admin.register(VideoCallBooking)
class VideoCallBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'location_link', 'booking_type', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('booking_type', 'status')
    search_fields = ('full_name', 'phone', 'location')
    readonly_fields = ('created_at', 'session_key')

    def location_link(self, obj):
        if not obj.location:
            return '—'
        url = f"https://www.google.com/maps/search/?api=1&query={quote(obj.location)}"
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, obj.location)
    location_link.short_description = 'Location'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'reseller_name', 'phone', 'city', 'total_amount', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('reseller_name', 'phone', 'city')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
