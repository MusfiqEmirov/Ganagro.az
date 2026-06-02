import html as html_lib
import logging
from email.utils import formataddr

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils import timezone
from django.utils.formats import date_format

from projects.utils.normalize_phone_number import normalize_az_phone

logger = logging.getLogger(__name__)


def _phone_whatsapp_href(phone):
    """Form nömrəsindən WhatsApp söhbət linki (wa.me)."""
    s = str(phone).strip()
    if not s:
        return ''

    normalized = normalize_az_phone(s)
    if normalized:
        return f'https://wa.me/994{normalized}'

    digits = ''.join(c for c in s if c.isdigit())
    if not digits:
        return ''
    if digits.startswith('994'):
        slug = digits
    elif digits.startswith('0'):
        slug = f'994{digits[1:]}'
    elif len(digits) == 9:
        slug = f'994{digits}'
    else:
        slug = digits
    return f'https://wa.me/{slug}'


def format_appeal_contact_message(instance):
    created_at = instance.created_at
    if timezone.is_aware(created_at):
        created_at = timezone.localtime(created_at)
    created_label = date_format(created_at, 'd.m.Y H:i')

    if instance.phone and instance.phone.strip():
        phone_raw = instance.phone.strip()
        wa_url = _phone_whatsapp_href(phone_raw)
        phone = f'{phone_raw} ({wa_url})' if wa_url else phone_raw
    else:
        phone = '—'

    return (
        f'Ad soyad:     {instance.full_name}\n'
        f'Mobil növrə:  {phone}\n'
        f'Mövzu:        {instance.subject}\n\n'
        'Mesaj:\n'
        f'{instance.info}\n\n'
        '────────────────────────────\n'
        f'Göndərilmə tarixi: {created_label}'
    )


def format_appeal_contact_message_html(instance):
    created_at = instance.created_at
    if timezone.is_aware(created_at):
        created_at = timezone.localtime(created_at)
    created_label = date_format(created_at, 'd.m.Y H:i')

    full_name = html_lib.escape(instance.full_name)
    subject = html_lib.escape(instance.subject)
    info = html_lib.escape(instance.info).replace('\n', '<br>')

    if instance.phone and instance.phone.strip():
        phone_raw = instance.phone.strip()
        phone_display = html_lib.escape(phone_raw)
        wa_href = html_lib.escape(_phone_whatsapp_href(phone_raw))
        if wa_href:
            phone_line = f'Mobil nömrə:  <a href="{wa_href}">{phone_display}</a>'
        else:
            phone_line = f'Mobil nömrə:  {phone_display}'
    else:
        phone_line = 'Mobil nömrə:  —'

    return (
        '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.6;">'
        f'<p style="margin:0;">Ad soyad: &nbsp;&nbsp;&nbsp;&nbsp; {full_name}</p>'
        f'<p style="margin:0;">{phone_line}</p>'
        f'<p style="margin:0;">Mövzu: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {subject}</p>'
        '<p style="margin:16px 0 0;">Mesaj:</p>'
        f'<p style="margin:0;">{info}</p>'
        '<hr style="border:none;border-top:1px solid #ccc;margin:16px 0;">'
        f'<p style="margin:0;">Göndərilmə tarixi: {created_label}</p>'
        '</div>'
    )

def send_appeal_contact_notification(instance):
    try:
        subject = 'Saytdan gələn müraciət'
        message = format_appeal_contact_message(instance)
        html_message = format_appeal_contact_message_html(instance)
        recipient = settings.CONTACT_RECEIVER_EMAIL
        if not recipient:
            logger.warning('Contact form email skipped: CONTACT_RECEIVER_EMAIL is not set.')
            return
        send_mail_func(
            recipient=recipient,
            subject=subject,
            message=message,
            html_message=html_message,
            sender_name=instance.full_name,
            sender_email=instance.email,
        )
    except Exception:
        logger.exception('Contact form notification email failed.')


def send_mail_func(
    recipient,
    subject,
    message,
    sender_name='',
    sender_email='',
    html_message=None,
):
    smtp_user = getattr(settings, 'EMAIL_HOST_USER', None) or settings.DEFAULT_FROM_EMAIL

    if sender_email:
        from_email = formataddr((sender_email, smtp_user))
        reply_to = [sender_email]
    else:
        from_email = smtp_user
        reply_to = []

    if html_message:
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[recipient],
            reply_to=reply_to,
        )
        email.attach_alternative(html_message, 'text/html')
    else:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[recipient],
            reply_to=reply_to,
        )
    email.send(fail_silently=False)
