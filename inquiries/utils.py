import re
from datetime import date, timedelta

from .models import ContactSubmission, VideoCallBooking


def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw or '')
    return digits[-10:]  # keep last 10 digits, drops country code/leading 0


def get_customer_activity(customer):
    from pages.models import Testimonial

    phone = customer.phone
    return {
        'enquiries': ContactSubmission.objects.filter(phone__contains=phone[-10:]),
        'video_calls': VideoCallBooking.objects.filter(phone__contains=phone[-10:], booking_type='video_call'),
        'appointments': VideoCallBooking.objects.filter(phone__contains=phone[-10:], booking_type='appointment'),
        # Testimonial doesn't collect a phone number, so this is a best-effort
        # name match only — a known limitation, not a bug.
        'reviews': Testimonial.objects.filter(name__icontains=customer.name) if customer.name else Testimonial.objects.none(),
    }


def needs_followup(customer, activity=None):
    if customer.next_followup_date and customer.next_followup_date <= date.today():
        return True
    activity = activity if activity is not None else get_customer_activity(customer)
    cutoff = date.today() - timedelta(days=2)
    stale_pending = (
        activity['video_calls'].filter(status='pending', created_at__date__lt=cutoff).exists()
        or activity['appointments'].filter(status='pending', created_at__date__lt=cutoff).exists()
    )
    return stale_pending and customer.stage == 'new'
