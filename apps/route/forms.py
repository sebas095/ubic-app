from mongodbforms import *
from django.utils.translation import ugettext as _
from .models import Route
import json
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

    def save(self, commit=True):
        route = super(RouteForm, self).save(commit=False)
        meta_clients = self.cleaned_data['meta_clients']
        route.clients = json.loads(meta_clients)

        if commit:
            route.save()
        return route