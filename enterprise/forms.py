from django import forms
from .models import Enterprise, User

class EnterpriseForm(forms.ModelForm):

    required_css_class = 'required'
    admin_by = forms.ModelChoiceField(queryset=User.objects.filter(enterprise=None).order_by('username'))


    class Meta: 
        model = Enterprise
        exclude = {'is_active'}