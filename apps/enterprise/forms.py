from django import forms
from django.utils.translation import ugettext as _
from .models import Enterprise, User

class EnterpriseForm(forms.ModelForm):

    required_css_class = 'required'
    admin_by = forms.ModelChoiceField(queryset=User.objects.filter(enterprise=None).order_by('username'))

    class Meta:
        model = Enterprise
        exclude = {'is_active', 'created_at'}


        widgets = {
            'nit': forms.HiddenInput()
        }

class EnterpriseEditForm(forms.ModelForm):

    class Meta:
        model = Enterprise
        exclude = {'nit', 'is_active', 'created_at'}

class DeactiveEnterpriseForm(forms.ModelForm):

    class Meta:
        model = Enterprise
        fields = ('is_active',)
        labels = {'is_active': 'Activo'}

    def __init__(self, *args, **kwargs):
        super(DeactiveEnterpriseForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = _(
            "Desmarque esta casilla si está seguro de que desea desactivar esta empresa del sistema.")

