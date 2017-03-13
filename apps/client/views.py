from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import ClientForm, ClientEditForm, DeactiveClientForm
from .models import Client

# Create your views here.
class ClientCreateView(CreateView):
    form_class = ClientForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

class ClientUpdateView(UpdateView):
    form_class = ClientEditForm
    model = Client
    template_name = "client_form.html"
    success_url = reverse_lazy("client_list")

class ClientListView(ListView):
    template_name = "clientlist.html"

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Client.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Client.objects.filter(enterprise__admin_by__username=self.request.user.username)

        else:
            return Client.objects.none()

class ClientDeactivateView(UpdateView):
    form_class = DeactiveClientForm
    model = Client
    template_name = "deactivate_client.html"
    success_url = reverse_lazy("client_list")
