from django import forms
from mongodbforms import *
from django.utils.translation import ugettext as _
from .models import Event, Loan
from apps.route.models import Route
from datetimewidget.widgets import DateWidget

class EventForm(DocumentForm):
    required_css_class = 'required'

    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'autoclose': True,
        'showMeridian': True
    }

    event_date = DateTimeField(
        widget=DateWidget(attrs={'id': "id_event_date"}, bootstrap_version=3, options=dateTimeOptions))

    class Meta:
        document = Event
        fields = ['event_date', 'description', 'type']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)
        event.created_by = self.user
        route = Route.objects()[0]
        if route:
            event.route_id = str(route.id)

        if commit:
            event.save()
        return event

class LoanForm(DocumentForm):
    required_css_class = 'required'

    class Meta:
        document = Loan
        fields = ['total_amount', 'payment_fee', 'rate', 'collection', 'event']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(LoanForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        loan = super(LoanForm, self).save(commit=False)
        loan.created_by = self.user

        if commit:
            loan.save()
        return loan