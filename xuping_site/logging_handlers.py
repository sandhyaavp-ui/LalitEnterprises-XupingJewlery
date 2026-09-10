import requests
from django.conf import settings
from django.utils.log import AdminEmailHandler


class ResendAdminEmailHandler(AdminEmailHandler):
    """Same traceback/request formatting as Django's AdminEmailHandler, but
    delivered via Resend's HTTP API instead of django.core.mail — this
    project has no working SMTP backend (Railway blocks outbound SMTP)."""

    def send_mail(self, subject, message, *args, fail_silently=False, html_message=None, **kwargs):
        if not settings.RESEND_API_KEY or not settings.ADMINS:
            return
        try:
            payload = {
                'from': 'Lalit Enterprises <onboarding@resend.dev>',
                'to': [email for _, email in settings.ADMINS],
                'subject': subject,
                'text': message,
            }
            if html_message:
                payload['html'] = html_message
            requests.post(
                'https://api.resend.com/emails',
                headers={'Authorization': f'Bearer {settings.RESEND_API_KEY}'},
                json=payload,
                timeout=10,
            )
        except requests.RequestException:
            pass
