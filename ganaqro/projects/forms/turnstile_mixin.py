from django import forms
from django.utils.translation import gettext_lazy as _

from projects.utils.turnstile_utils import is_turnstile_configured, verify_turnstile_response


class TurnstileMixin:
    """
    Cloudflare Turnstile checkbox validation.
    Widget `cf-turnstile-response` POST edir.
    """

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._turnstile_request = request
        self.fields.setdefault(
            'turnstile',
            forms.CharField(required=False, widget=forms.HiddenInput(), label=''),
        )

    def _turnstile_is_enabled(self) -> bool:
        return is_turnstile_configured()

    def _turnstile_verify(self) -> bool:
        if not self._turnstile_is_enabled():
            return True

        token = (self.data.get('cf-turnstile-response') or '').strip()
        if not token:
            self.add_error('turnstile', _('Please verify that you are human.'))
            return False

        remote_ip = None
        req = getattr(self, '_turnstile_request', None)
        if req is not None:
            remote_ip = req.META.get('REMOTE_ADDR')

        ok = verify_turnstile_response(token, remote_ip=remote_ip)
        if not ok:
            self.add_error('turnstile', _('Captcha verification failed. Please try again.'))
        return ok
