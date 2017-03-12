from django.views.generic import TemplateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class RoutePageView(TemplateView):
    template_name = "routes.html"