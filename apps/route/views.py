from django.views.generic import TemplateView, UpdateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login
from .models import Route
from .forms import RouteForm

# Create your views here.
@require_login
@require_service
class RoutePageView(TemplateView):
    template_name = "routes.html"

@require_login
@require_service
class RouteCreateView(CreateView):
    form_class = RouteForm
    model = Route
    template_name = "route_form.html"
    success_url = reverse_lazy('route_index')