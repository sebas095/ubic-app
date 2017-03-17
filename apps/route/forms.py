from mongodbforms import *
from django.utils.translation import ugettext as _
from .models import Route

from django.forms import HiddenInput, TextInput

class RouteForm(DocumentForm):

    meta_clients = MongoCharField()
    class Meta:
        document = Route
        fields = ["name", "directions", "clients"]
        widgets = {
            'name': TextInput(attrs={'placeholder': _("Name for the route")}),
            'directions': HiddenInput(),
            'meta_clients': HiddenInput()
        }
