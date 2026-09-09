import requests
from django.conf import settings


def send_notification_email(subject, message):
    """Send a plain-text notification via Resend's HTTP API.

    Swallows any failure the same way the old send_mail(fail_silently=True)
    calls did — a missing key or a Resend-side error should never break the
    form submission it's notifying about.
    """
    if not settings.RESEND_API_KEY or not settings.NOTIFY_EMAIL:
        return
    try:
        requests.post(
            'https://api.resend.com/emails',
            headers={'Authorization': f'Bearer {settings.RESEND_API_KEY}'},
            json={
                'from': 'Lalit Enterprises <onboarding@resend.dev>',
                'to': [settings.NOTIFY_EMAIL],
                'subject': subject,
                'text': message,
            },
            timeout=10,
        )
    except requests.RequestException:
        pass
