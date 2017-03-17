from mongodbforms import *
from django.utils.translation import ugettext as _
from .models import Route

from django.forms import HiddenInput, TextInput

class RouteForm(DocumentForm):
    class Meta:
        document = Route
        fields = ["name", "route"]
        widgets = {
            'name': TextInput(attrs={'placeholder': _("Name for the route")}),
            'route': HiddenInput()
        }
