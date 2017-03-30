from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.http import HttpResponseRedirect
from .models import Event
from .forms import EventForm
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login

# Create your views here.
@require_login
@require_service
class EventCreateView(CreateView):
    template_name = "event_form.html"
    form_class = EventForm
    document = Event
    success_url = reverse_lazy('event_list')

    def get_form_kwargs(self):
        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user.username})
        return kwargs

@require_login
@require_service
class EventUpdateView(UpdateView):
    template_name = "event_form.html"
    form_class = EventForm
    document = Event
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        return Event.objects(id=self.kwargs['id'])[0]

    def get_form_kwargs(self):
        kwargs = super(EventUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user.username})
        return kwargs

@require_login
@require_service
class EventListView(ListView):
    template_name = "eventlist.html"
    document = Event

    def get_queryset(self):
        return Event.objects(created_by=self.request.user.username)

@require_login
@require_service
class EventDeleteView(DeleteView):
    document = Event
    template_name = "delete_event.html"
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        return Event.objects(id=self.kwargs['id'])[0]