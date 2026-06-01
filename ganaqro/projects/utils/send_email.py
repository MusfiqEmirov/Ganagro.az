import logging
from email.utils import formataddr

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.formats import date_format

logger = logging.getLogger(__name__)


def format_appeal_contact_message(instance):
    created_at = instance.created_at
    if timezone.is_aware(created_at):
        created_at = timezone.localtime(created_at)
    created_label = date_format(created_at, 'd.m.Y H:i')

    phone = instance.phone.strip() if instance.phone else '—'

    return (
        'Yeni əlaqə formu müraciəti\n'
        '────────────────────────────\n\n'
        f'Ad soyad:     {instance.full_name}\n'
        f'Mobil nömrə:  {phone}\n\n'
        'Mesaj:\n'
        f'{instance.info}\n\n'
        '────────────────────────────\n'
        f'Göndərilmə tarixi: {created_label}'
    )


def send_appeal_contact_notification(instance):
    try:
        subject = 'Saytdan gələn müraciət'
        message = format_appeal_contact_message(instance)
        recipient = settings.CONTACT_RECEIVER_EMAIL
        if not recipient:
            logger.warning('Contact form email skipped: CONTACT_RECEIVER_EMAIL is not set.')
            return
        send_mail_func(
            recipient=recipient,
            subject=subject,
            message=message,
            sender_name=instance.full_name,
            sender_email=instance.email,
        )
    except Exception:
        logger.exception('Contact form notification email failed.')


def send_mail_func(recipient, subject, message, sender_name='', sender_email=''):
    smtp_user = getattr(settings, 'EMAIL_HOST_USER', None) or settings.DEFAULT_FROM_EMAIL

    if sender_email:
        from_email = formataddr((sender_email, smtp_user))
        reply_to = [sender_email]
    else:
        from_email = smtp_user
        reply_to = []

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[recipient],
        reply_to=reply_to,
    )
    email.send(fail_silently=False)
