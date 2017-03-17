from django.views.generic import View, UpdateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from utils.decorators import require_service, require_login
from .models import Route
from apps.client.models import Client
from .forms import RouteForm

# Create your views here.
@require_login
@require_service
class RoutePageView(View):
    template_name = "routes.html"

    def get(self, request):
        clients = Client.objects.filter(enterprise__admin_by__username=request.user.username)
        return render(request, 'routes.html', {
            "clients": clients
        })

@require_login
@require_service
class RouteCreateView(CreateView):
    form_class = RouteForm
    document = Route
    template_name = "route_form.html"
    success_url = "/"