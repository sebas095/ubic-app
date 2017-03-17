from django.views.generic import View, UpdateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils.decorators import require_service, require_login
from apps.client.models import Client
from .forms import RouteForm
from .models import Route

# Create your views here.
@require_login
@require_service
class RoutePageView(CreateView):
    template_name = "routes.html"
    form_class = RouteForm
    document = Route
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(RoutePageView, self).get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(enterprise__admin_by__username=self.request.user.username)
        return context

@require_login
@require_service
class RouteUpdateView(UpdateView):
    template_name = "edit_route.html"
    form_class = RouteForm
    document = Route
    success_url = '/'
