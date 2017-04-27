from mongodbforms import *
from django.utils.translation import ugettext as _
from .models import Route
import json
from django.forms import HiddenInput, TextInput

class RouteForm(DocumentForm):
    enterprise = ""

    meta_clients = MongoCharField()
    class Meta:
        document = Route
        fields = ["name", "directions", "clients"]
        widgets = {
            'name': TextInput(attrs={'placeholder': _("Name for the route"), 'class': 'form-control'}),
            'directions': HiddenInput(),
            'meta_clients': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.enterprise = kwargs.pop("enterprise")
        super(RouteForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        route = super(RouteForm, self).save(commit=False)
        meta_clients = self.cleaned_data['meta_clients']
        route.clients = json.loads(meta_clients)
        route.enterprise = self.enterprise

        if commit:
            route.save()
        return route