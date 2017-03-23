from __future__ import unicode_literals
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class TrixEditor(forms.Textarea):

    def __init__(self,
                 *args,
                 params={},
                 toolbar_template=None,
                 **kwargs):
        self.params = params.copy()
        self.toolbar_template = toolbar_template
        super(TrixEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        if attrs is None:
            attrs = {}
        attrs.update({'style': 'visibility: hidden; position: absolute;'})

        self.params.update({
            'input': (self.params.get('input') or
                      attrs.get('id') or
                      '{}_id'.format(name)),
            'class': ' '.join(
                self.params.get('class', '').split(' ') + ['trix-content']
            ),
        })
        if self.toolbar_template:
            self.params.update({
                'toolbar': self.params.get(
                    'toolbar',
                    'trix-{name}-toolbar'.format(name=name)
                )
            })

        param_str = ' '.join('{}="{}"'.format(k, v)
                             for k, v in self.params.items())

        textarea = super(TrixEditor, self).render(name, value, attrs)

        return render_to_string(
            'trix/widget.html',
            context={
                'toolbar_id': self.params.get('toolbar'),
                'textarea': textarea,
                'toolbar_template': self.toolbar_template,
                'params': mark_safe(param_str),
            }
        )

    class Media:
        css = {'all': ('trix/trix.css',)}
        js = ('trix/trix.js', 'trix/trix-django.js')
