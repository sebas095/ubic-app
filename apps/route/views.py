from django.views.generic import DeleteView, UpdateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login
from .forms import RouteForm
from .models import Route
from apps.enterprise.models import Enterprise
from apps.client.models import Client
from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import RouteSerializer
from django.http import HttpResponse


# Create your views here.
@require_login
@require_service
class RoutePageView(CreateView):
    template_name = "routes.html"
    form_class = RouteForm
    document = Route
    success_url = reverse_lazy('route_list')

    def get_context_data(self, **kwargs):
        context = super(RoutePageView, self).get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(enterprise__admin_by__username=self.request.user.username)
        return context

    def get_form_kwargs(self):
        nit = Enterprise.objects.filter(admin_by__username=self.request.user.username)[0].nit
        kwargs = super(RoutePageView, self).get_form_kwargs()
        kwargs.update({"enterprise": nit})
        return kwargs


@require_login
@require_service
class RouteUpdateView(UpdateView):
    template_name = "edit_route.html"
    form_class = RouteForm
    document = Route
    success_url = reverse_lazy('route_list')

    def get_object(self, queryset=None):
        return Route.objects(id=self.kwargs['id'])[0]

    def get_context_data(self, **kwargs):
        context = super(RouteUpdateView, self).get_context_data(**kwargs)
        nit = Enterprise.objects.filter(admin_by__username=self.request.user.username)[0].nit
        route = Route.objects(enterprise=nit)[0]
        context["clients"] = list(map(lambda id: Client.objects.get(id=id), route.clients))
        return context

    def get_form_kwargs(self):
        nit = Enterprise.objects.filter(admin_by__username=self.request.user.username)[0].nit
        kwargs = super(RouteUpdateView, self).get_form_kwargs()
        kwargs.update({"enterprise": nit})
        return kwargs

@require_login
@require_service
class RouteDeleteView(DeleteView):
    document = Route
    template_name = "delete_route.html"
    success_url = reverse_lazy('route_list')

    def get_object(self, queryset=None):
        return Route.objects(id=self.kwargs['id'])[0]

@require_login
@require_service
class RouteListView(ListView):
    document = Route
    template_name = "routelist.html"

    def get_queryset(self):
        nit = Enterprise.objects.filter(admin_by__username=self.request.user.username)[0].nit
        return Route.objects(enterprise=nit)

@require_login
@require_service
class RouteAPI(ModelViewSet):
    lookup_field = 'id'
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects()