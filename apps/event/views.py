from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .models import Event, Loan
from .forms import EventForm, LoanForm
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# Create your views here.
@require_login
@require_service
class EventCreateView(CreateView):
    template_name = "event/event_form.html"
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
    template_name = "event/event_form.html"
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
    template_name = "event/eventlist.html"
    document = Event

    def get_queryset(self):
        return Event.objects(created_by=self.request.user.username)

@require_login
@require_service
class EventDeleteView(DeleteView):
    document = Event
    template_name = "event/delete_event.html"
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        return Event.objects(id=self.kwargs['id'])[0]

@require_login
@require_service
class LoanCreateView(CreateView):
    template_name = 'loan/loan_form.html'
    form_class = LoanForm
    model = Loan
    success_url = reverse_lazy('loan_list')

    def get_form_kwargs(self):
        kwargs = super(LoanCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user.username})
        return kwargs

@require_login
@require_service
class LoanUpdateView(UpdateView):
    template_name = "loan/loan_form.html"
    form_class = LoanForm
    document = Loan
    success_url = reverse_lazy('loan_list')

    def get_object(self, queryset=None):
        return Loan.objects(id=self.kwargs['id'])[0]

    def get_form_kwargs(self):
        kwargs = super(LoanUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user.username})
        return kwargs

@require_login
@require_service
class LoanDeleteView(DeleteView):
    document = Loan
    template_name = "loan/delete_loan.html"
    success_url = reverse_lazy('loan_list')

    def get_object(self, queryset=None):
        return Loan.objects(id=self.kwargs['id'])[0]

@require_login
@require_service
class LoanListView(ListView):
    template_name = "loan/loanlist.html"
    document = Loan

    def get_queryset(self):
        return Loan.objects(created_by=self.request.user.username)

class EventAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(template_name='event/event_form.html')

