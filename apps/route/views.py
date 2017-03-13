from django.views.generic import TemplateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@require_service
class RoutePageView(TemplateView):
    template_name = "routes.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RoutePageView, self).dispatch(*args, **kwargs)