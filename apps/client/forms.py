from django import forms
from django.utils.translation import ugettext as _
from .models import Client

class ClientForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Client
        exclude = {'is_active'}

class ClientEditForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = {'is_active'}

class DeactiveClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('is_active',)
        labels = {'is_active': 'Activo'}

    def __init__(self, *args, **kwargs):
        super(DeactiveClientForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = _(
            "Desmarque esta casilla si está seguro de que desea desactivar este cliente del sistema.")