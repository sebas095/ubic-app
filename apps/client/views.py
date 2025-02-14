from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import ClientForm, DeactiveClientForm
from .models import Client
from utils.decorators import require_service, require_login

# Create your views here.
@require_login
@require_service
class ClientCreateView(CreateView):
    form_class = ClientForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

    def get_form_kwargs(self):
        kwargs = super(ClientCreateView, self).get_form_kwargs()
        kwargs.update({"admin_by": self.request.user})
        return kwargs


@require_login
@require_service
class ClientUpdateView(UpdateView):
    form_class = ClientForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

    def get_form_kwargs(self):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs.update({"admin_by": self.request.user})
        return kwargs


@require_login
@require_service
class ClientListView(ListView):
    template_name = "clientlist.html"

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Client.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Client.objects.filter(enterprise__admin_by__username=self.request.user.username)

        else:
            return Client.objects.none()

@require_login
@require_service
class ClientDeactivateView(UpdateView):
    form_class = DeactiveClientForm
    model = Client
    template_name = "deactivate_client.html"
    success_url = reverse_lazy("client_list")
