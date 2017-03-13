from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import ClientForm, ClientEditForm, DeactiveClientForm
from .models import Client
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.decorators import require_service

# Create your views here.
@require_service
class ClientCreateView(CreateView):
    form_class = ClientForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClientCreateView, self).dispatch(*args, **kwargs)

@require_service
class ClientUpdateView(UpdateView):
    form_class = ClientEditForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClientUpdateView, self).dispatch(*args, **kwargs)

@require_service
class ClientListView(ListView):
    template_name = "clientlist.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClientListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Client.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Client.objects.filter(enterprise__admin_by__username=self.request.user.username)

        else:
            return Client.objects.none()

@require_service
class ClientDeactivateView(UpdateView):
    form_class = DeactiveClientForm
    model = Client
    template_name = "deactivate_client.html"
    success_url = reverse_lazy("client_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClientDeactivateView, self).dispatch(*args, **kwargs)
