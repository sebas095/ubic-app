from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .models import Event, Loan
from apps.route.models import Route
from apps.enterprise.models import Enterprise
from .forms import EventForm, LoanForm
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from bson import ObjectId
from datetime import datetime, timedelta

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
        nit = Enterprise.objects.filter(admin_by__username=request.user.username)[0].nit
        routes = Route.objects(enterprise=nit)
        routes = list(map(lambda r: r.name + '^' + str(r.id), routes))
        form = {'route': routes}
        return Response({'form': form}, template_name='event/event_form.html')

class EventCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        date = datetime.strptime(request.POST['event_date'], '%Y-%m-%d %H:%M:%S')
        routes = request.POST.getlist('routes[]')
        routes = list(map(lambda r: ObjectId(r), routes))

        data = {
            'created_by': request.user.username,
            'event_date':  date.isoformat(),
            'description': request.POST['description'],
            'type': request.POST['type'],
            'route': routes,
        }
        event = EventSerializer(data=data)

        if event.is_valid():
            event.save()
            ev = Event.objects(
                created_by=request.user.username,
                description=request.POST['description'],
                type=request.POST['type'],
            )
            my_tyme = (date + timedelta(hours=5)).isoformat()
            ev = list(filter(lambda e: e.event_date.isoformat() == my_tyme, ev))[0]

            return Response({'ok': True, 'id': str(ev.id)}, status=status.HTTP_201_CREATED)
        return Response(event.errors, status=status.HTTP_400_BAD_REQUEST)