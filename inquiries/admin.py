from django.contrib import admin
from .models import ContactSubmission, VideoCallBooking, Order, OrderItem


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'submitted_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('submitted_at',)


@admin.register(VideoCallBooking)
class VideoCallBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'location', 'booking_type', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('booking_type', 'status')
    search_fields = ('full_name', 'phone')
    readonly_fields = ('created_at', 'session_key')


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
