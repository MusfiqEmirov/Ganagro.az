from django import forms


class BootstrapIconSelect(forms.Select):
    class Media:
        css = {
            'all': (
                'assets/vendor/bootstrap-icons/bootstrap-icons.css',
                'assets/css/admin_icon_select.css',
            ),
        }
        js = ('assets/js/admin_icon_select.js',)

    def __init__(self, attrs=None, choices=()):
        attrs = dict(attrs or {})
        css_class = attrs.get('class', '')
        attrs['class'] = f'{css_class} bootstrap-icon-select'.strip()
        super().__init__(attrs=attrs, choices=choices)
