from django.conf import settings


def turnstile(request):
    site_key = (getattr(settings, 'TURNSTILE_SITE_KEY', '') or '').strip()
    secret_key = (getattr(settings, 'TURNSTILE_SECRET_KEY', '') or '').strip()
    return {
        'turnstile_enabled': bool(site_key and secret_key),
        'turnstile_site_key': site_key,
    }
