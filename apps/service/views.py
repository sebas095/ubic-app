from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import ServiceForm, ServiceEditForm, DeactiveServiceForm
from.models import Service

# Create your views here.
class ServiceCreateView(CreateView):
    form_class = ServiceForm
    model = Service
    template_name = "enterprise_form.html"
    success_url = reverse_lazy("service_list")

class ServiceUpdateView(UpdateView):
    form_class = ServiceEditForm
    model = Service
    template_name = "service_edit_form.html"
    success_url = reverse_lazy("service_list")

class ServiceListView(ListView):
    template_name = "servicelist.html"

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Service.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Service.objects.filter(is_active=True, enterprise__admin_by=self.request.user.username)

        else:
            return Service.objects.none()

class ServiceDeactivateView(UpdateView):
    form_class = DeactiveServiceForm
    model = Service
    template_name = "deactivate_service.html"
    success_url = reverse_lazy("service_list")