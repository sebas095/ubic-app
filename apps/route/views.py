from django.views.generic import TemplateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login

# Create your views here.
@require_login
@require_service
class RoutePageView(TemplateView):
    template_name = "routes.html"