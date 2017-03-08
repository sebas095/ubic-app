from django import forms
from django.utils.translation import ugettext as _
from .models import Service

class ServiceForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Service
        exclude = {'is_active'}

class ServiceEditForm(forms.ModelForm):

    class Meta:
        model = Service
        exclude = {'is_active'}

class DeactiveServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('is_active',)
        labels = {'is_active': 'Activo'}

    def __init__(self, *args, **kwargs):
        super(DeactiveServiceForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = _(
            "Desmarque esta casilla si está seguro de que desea desactivar este servicio del sistema.")
