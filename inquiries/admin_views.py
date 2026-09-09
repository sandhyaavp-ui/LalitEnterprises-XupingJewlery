from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import VideoCallBooking, ContactSubmission, Customer
from .utils import get_customer_activity, needs_followup
from pages.models import Testimonial


@staff_member_required
def dashboard(request):
    video_calls = VideoCallBooking.objects.filter(booking_type='video_call').order_by('-created_at')
    appointments = VideoCallBooking.objects.filter(booking_type='appointment').order_by('-created_at')
    enquiries = ContactSubmission.objects.order_by('-submitted_at')
    reviews = Testimonial.objects.order_by('-submitted_at')

    customers = []
    for customer in Customer.objects.all():
        activity = get_customer_activity(customer)
        customers.append({
            'obj': customer,
            'activity': activity,
            'needs_followup': needs_followup(customer, activity),
        })
    customers.sort(key=lambda c: not c['needs_followup'])

    return render(request, 'inquiries/dashboard.html', {
        'video_calls': video_calls,
        'appointments': appointments,
        'enquiries': enquiries,
        'reviews': reviews,
        'customers': customers,
        'video_calls_pending': video_calls.filter(status='pending').count(),
        'video_calls_confirmed': video_calls.filter(status='confirmed').count(),
        'video_calls_completed': video_calls.filter(status='completed').count(),
        'video_calls_cancelled': video_calls.filter(status='cancelled').count(),
        'appointments_pending': appointments.filter(status='pending').count(),
        'appointments_confirmed': appointments.filter(status='confirmed').count(),
        'appointments_completed': appointments.filter(status='completed').count(),
        'appointments_cancelled': appointments.filter(status='cancelled').count(),
        'reviews_pending': reviews.filter(approved=False).count(),
        'reviews_approved': reviews.filter(approved=True).count(),
        'customers_needs_followup': sum(1 for c in customers if c['needs_followup']),
        'customers_total': len(customers),
    })


@staff_member_required
@require_POST
def update_booking_status(request, booking_id):
    booking = get_object_or_404(VideoCallBooking, pk=booking_id)
    new_status = request.POST.get('status')
    valid = dict(VideoCallBooking.STATUS_CHOICES)
    if new_status not in valid:
        return JsonResponse({'error': 'invalid status'}, status=400)
    booking.status = new_status
    booking.save()
    return JsonResponse({'status': 'ok', 'new_status': new_status})


@staff_member_required
@require_POST
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if 'stage' in request.POST:
        new_stage = request.POST['stage']
        valid = dict(Customer.STAGE_CHOICES)
        if new_stage not in valid:
            return JsonResponse({'error': 'invalid stage'}, status=400)
        customer.stage = new_stage
    if 'notes' in request.POST:
        customer.notes = request.POST['notes']
    if 'next_followup_date' in request.POST:
        customer.next_followup_date = request.POST['next_followup_date'] or None
    customer.save()
    return JsonResponse({'status': 'ok'})
