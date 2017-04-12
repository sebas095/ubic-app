from django.views.generic import DeleteView, UpdateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login
from .forms import RouteForm
from .models import Route
from apps.enterprise.models import Enterprise
from apps.client.models import Client
from rest_framework_mongoengine.viewsets import GenericAPIView
from .serializers import RouteSerializer
from django.http import HttpResponse
import json

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

# @require_login
# @require_service
class RouteListAPI(GenericAPIView):
    lookup_field = 'id'
    serializer_class = RouteSerializer

    def get(self, request):
        nit = Enterprise.objects.filter(admin_by__username= 'sebas.duque')[0].nit  # request.user.username)[0].nit
        routes = Route.objects(enterprise=nit)
        routes = list(map(self.filter, routes))
        return HttpResponse(json.dumps(routes), content_type='application/json')

    def filter(self, item):
        return {
            "id": str(item.id),
            "created_at": str(item.created_at),
            "name": item.name,
            "enterprise": item.enterprise
        }


# @require_login
# @require_service
class RouteAPI(GenericAPIView):
    lookup_field = 'id'
    serializer_class = RouteSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        route = Route.objects(id=id)[0]
        route.clients_data = list(map(lambda pk: Client.objects.get(id=pk), route.clients))
        del route.clients
        route.clients_data = list(map(lambda client: {
            "fullname": client.fullname,
            "document": client.document,
            "phone": client.phone,
            "address": client.address,
            "email": client.email,
            "lat": client.lat,
            "lng": client.lon
        }, route.clients_data))
        return HttpResponse(route.to_json(), content_type='application/json')