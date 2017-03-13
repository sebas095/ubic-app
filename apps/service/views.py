from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import ServiceForm, DeactiveServiceForm
from.models import Service
from utils.decorators import require_service
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@require_service
class ServiceCreateView(CreateView):
    form_class = ServiceForm
    model = Service
    template_name = "service_form.html"
    success_url = reverse_lazy("service_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServiceCreateView, self).dispatch(*args, **kwargs)

@require_service
class ServiceUpdateView(UpdateView):
    form_class = ServiceForm
    model = Service
    template_name = "service_form.html"
    success_url = reverse_lazy("service_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServiceUpdateView, self).dispatch(*args, **kwargs)

@require_service
class ServiceListView(ListView):
    template_name = "servicelist.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServiceListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Service.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Service.objects.filter(is_active=True, enterprise__admin_by__username=self.request.user.username)

        else:
            return Service.objects.none()

@require_service
class ServiceDeactivateView(UpdateView):
    form_class = DeactiveServiceForm
    model = Service
    template_name = "deactivate_service.html"
    success_url = reverse_lazy("service_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServiceDeactivateView, self).dispatch(*args, **kwargs)