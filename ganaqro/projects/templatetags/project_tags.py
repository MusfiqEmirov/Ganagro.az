import html as html_lib
import re
from urllib.parse import parse_qs, quote_plus, urlparse

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


def _plain_text(value):
    """CKEditor HTML → kart üçün təmiz mətn."""
    if value is None:
        return ''
    raw = str(value)
    raw = re.sub(r'<\s*br\s*/?\s*>', ' ', raw, flags=re.I)
    raw = re.sub(r'</\s*(p|div|li|h[1-6]|blockquote|tr|td|th)\s*>', ' ', raw, flags=re.I)
    text = strip_tags(raw)
    text = html_lib.unescape(text)
    text = text.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()


@register.filter
def tel_href(value):
    """
    Normalize phone field for tel: links (digits and leading + only).
    """
    if value is None:
        return ''
    s = str(value).strip()
    if not s:
        return ''
    if s.lower().startswith('tel:'):
        return mark_safe(s)
    chars = []
    plus_used = False
    for i, c in enumerate(s):
        if c.isdigit():
            chars.append(c)
        elif c == '+' and not plus_used and not chars:
            chars.append('+')
            plus_used = True
    if not chars:
        return mark_safe('tel:' + s)
    return mark_safe('tel:' + ''.join(chars))


@register.filter
def mailto_href(value):
    """
    Normalize email text for mailto: links (strip whitespace / angle brackets).
    """
    if value is None:
        return ''
    s = str(value).strip().strip('"').strip("'")
    if not s:
        return ''
    if '<' in s:
        _, _, rest = s.partition('<')
        if '>' in rest:
            addr = rest.partition('>')[0].strip()
            if addr:
                s = addr
    if not s.startswith('mailto:'):
        return mark_safe('mailto:' + s.strip())
    return mark_safe(s)


@register.filter
def google_maps_url(value):
    """
    Open Google Maps search for a plain-text address.
    """
    if value is None:
        return ''
    s = str(value).strip()
    if not s:
        return ''
    return mark_safe(f'https://www.google.com/maps/search/?api=1&query={quote_plus(s)}')


@register.filter
def wa_me_url(value):
    """
    Build https://wa.me/<international_digits> for chat links.

    Stored values often include spaces, dashes or a leading '+' — wa.me
    expects digits only after the slash. HTTP(S) whatsapp URLs are rewritten
    when we can derive a canonical wa.me numeric path.
    """
    if value is None:
        return ''
    s = str(value).strip().rstrip('/')
    if not s:
        return ''
    lowered = s.lower()

    def _digits_only(raw):
        return ''.join(c for c in raw if c.isdigit())

    if lowered.startswith(('http://', 'https://')):
        parsed = urlparse(s)
        host = (parsed.netloc or '').split('@')[-1].lower()
        if host in {'wa.me', 'www.wa.me'}:
            slug = _digits_only(parsed.path)
            if slug:
                return mark_safe(f'https://wa.me/{slug}')
            return ''
        if 'chat.whatsapp.com' in host:
            return mark_safe(s)
        if 'whatsapp.com' in host and 'send' in (parsed.path or '').lower():
            phone = parse_qs(parsed.query).get('phone', ('',))[0]
            slug = _digits_only(phone)
            if slug:
                return mark_safe(f'https://wa.me/{slug}')
            return ''

    slug = _digits_only(s)
    if not slug:
        return ''
    return mark_safe(f'https://wa.me/{slug}')


@register.filter
def truncate_sentence(value, max_chars=500):
    """
    Plain text excerpt for cards: strips HTML, then truncates near max_chars.
    Prefers the last sentence end inside the limit; otherwise breaks at a word.
    """
    text = _plain_text(value)
    if not text:
        return text

    max_chars = int(max_chars)
    if len(text) <= max_chars:
        return text

    chunk = text[:max_chars]

    last_punct = max(chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?'))
    if last_punct > 0 and last_punct >= len(chunk) * 0.3:
        return chunk[:last_punct + 1].strip()

    last_space = chunk.rfind(' ')
    if last_space > 0:
        return chunk[:last_space].rstrip() + '…'

    return chunk.rstrip() + '…'


@register.filter
def plain_text(value):
    """CKEditor HTML field as plain text (for card previews)."""
    return _plain_text(value)
