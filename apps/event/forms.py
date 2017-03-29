from django import forms
from django.utils.translation import ugettext as _
from .models import Event

class HelpForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Event
        exclude = {}