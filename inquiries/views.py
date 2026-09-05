import json
from datetime import date

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET

from .forms import ContactForm, AppointmentForm, OrderForm, OrderItemFormSet
from .models import ContactSubmission, VideoCallBooking


def _get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def contact(request):
    if request.method == 'POST' and 'submit_enquiry' in request.POST:
        enquiry_form = ContactForm(request.POST)
        appointment_form = AppointmentForm()
        if enquiry_form.is_valid():
            enquiry_form.save()
            messages.success(request, "Thanks for your enquiry — we reply the same working day.")
            return redirect('inquiries:contact')
    elif request.method == 'POST' and 'submit_appointment' in request.POST:
        enquiry_form = ContactForm()
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            booking = appointment_form.save(commit=False)
            booking.session_key = _get_or_create_session_key(request)
            booking.booking_type = 'appointment'
            booking.save()
            messages.success(request, "Your appointment request has been received — we'll confirm by phone.")
            return redirect('inquiries:contact')
    else:
        enquiry_form = ContactForm()
        appointment_form = AppointmentForm()

    return render(request, 'inquiries/contact.html', {
        'enquiry_form': enquiry_form,
        'appointment_form': appointment_form,
    })


def video_call_booking(request):
    return render(request, 'inquiries/video_call_booking.html')


def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.payment_status = 'pending'
            order.save()
            formset.instance = order
            items = formset.save()

            total = sum(item.subtotal for item in order.items.all())
            order.total_amount = total
            order.save()

            messages.success(
                request,
                "Your order has been submitted. Our team will reach out on WhatsApp to confirm payment and dispatch."
            )
            return redirect('inquiries:order_form')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'inquiries/order_form.html', {'form': form, 'formset': formset})


@require_POST
@csrf_protect
def chatbot_enquiry(request):
    data = json.loads(request.body)
    ContactSubmission.objects.create(
        name=data.get('name', '').strip(),
        phone=data.get('phone', '').strip(),
        email='',
        message=data.get('message', '').strip(),
    )
    return JsonResponse({'status': 'ok'})


@require_POST
@csrf_protect
def book_video_call(request):
    data = json.loads(request.body)
    session_key = _get_or_create_session_key(request)
    VideoCallBooking.objects.create(
        full_name=data.get('full_name', '').strip(),
        location=data.get('location', '').strip(),
        phone=data.get('phone', '').strip(),
        preferred_date=data.get('date'),
        preferred_time=data.get('time', ''),
        session_key=session_key,
        booking_type='video_call',
    )
    return JsonResponse({'status': 'ok'})


@require_GET
def my_calls(request):
    session_key = request.session.session_key
    if not session_key:
        return JsonResponse({'upcoming': [], 'history': []})

    bookings = VideoCallBooking.objects.filter(
        session_key=session_key, booking_type='video_call'
    ).order_by('preferred_date')
    today = date.today()
    upcoming = [b for b in bookings if b.preferred_date >= today]
    history = [b for b in bookings if b.preferred_date < today]

    def serialize(b):
        return {
            'name': b.full_name,
            'date': str(b.preferred_date),
            'time': b.preferred_time,
            'location': b.location,
        }

    return JsonResponse({
        'upcoming': [serialize(b) for b in upcoming],
        'history': [serialize(b) for b in history],
    })
