from django import forms
from django.utils.translation import ugettext as _
from .models import Service
from datetimewidget.widgets import DateWidget

class ServiceForm(forms.ModelForm):
    required_css_class = 'required'

    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian': True
    }

    start_date = forms.DateField(widget=DateWidget(attrs={'id': "id_start_date"}, bootstrap_version=3, options=dateTimeOptions),
                    label=_("Fecha de inicio"), required=True)
    finish_date = forms.DateField(widget=DateWidget(attrs={'id': "id_finish_date"}, bootstrap_version=3, options=dateTimeOptions),
                    label=_("Fecha de finalización"), required=True)

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
