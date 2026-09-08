from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import VideoCallBooking, ContactSubmission


@staff_member_required
def dashboard(request):
    video_calls = VideoCallBooking.objects.filter(booking_type='video_call').order_by('-created_at')
    appointments = VideoCallBooking.objects.filter(booking_type='appointment').order_by('-created_at')
    enquiries = ContactSubmission.objects.order_by('-submitted_at')

    return render(request, 'inquiries/dashboard.html', {
        'video_calls': video_calls,
        'appointments': appointments,
        'enquiries': enquiries,
        'video_calls_pending': video_calls.filter(status='pending').count(),
        'video_calls_confirmed': video_calls.filter(status='confirmed').count(),
        'video_calls_completed': video_calls.filter(status='completed').count(),
        'video_calls_cancelled': video_calls.filter(status='cancelled').count(),
        'appointments_pending': appointments.filter(status='pending').count(),
        'appointments_confirmed': appointments.filter(status='confirmed').count(),
        'appointments_completed': appointments.filter(status='completed').count(),
        'appointments_cancelled': appointments.filter(status='cancelled').count(),
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
