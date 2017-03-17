from django import forms
from django.utils.translation import ugettext as _
from .models import Client, Enterprise


class ClientForm(forms.ModelForm):
    required_css_class = 'required'
    admin_by = ""
    observations = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Especifique informaciones adicionales para llegar al sitio')})
    )

    class Meta:
        model = Client
        exclude = {'is_active'}

        widgets = {
            'lat': forms.HiddenInput(),
            'lon': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.admin_by = kwargs.pop('admin_by')
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['enterprise'] = forms.ModelChoiceField(
            queryset=Enterprise.objects.filter(admin_by__username=self.admin_by.username))


class DeactiveClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('is_active',)
        labels = {'is_active': 'Activo'}

    def __init__(self, *args, **kwargs):
        super(DeactiveClientForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = _(
            "Desmarque esta casilla si está seguro de que desea desactivar este cliente del sistema.")
