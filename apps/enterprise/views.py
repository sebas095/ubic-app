from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import EnterpriseForm, EnterpriseEditForm, DeactiveEnterpriseForm
from.models import Enterprise

# Create your views here.
class EnterpriseCreateView(CreateView):
    form_class = EnterpriseForm
    model = Enterprise
    template_name = "enterprise_form.html"
    success_url = reverse_lazy("enterprise_list")

class EnterpriseUpdateView(UpdateView):
    form_class = EnterpriseEditForm
    model = Enterprise
    template_name = "enterprise_edit_form.html"
    success_url = reverse_lazy("enterprise_list")

class EnterpriseListView(ListView):
    template_name = "enterpriselist.html"

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Enterprise.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Enterprise.objects.filter(is_active=True)

        else:
            return Enterprise.objects.none()

class EnterpriseDeactivateView(UpdateView):
    form_class = DeactiveEnterpriseForm
    model = Enterprise
    template_name = "deactivate_enterprise_account.html"
    success_url = reverse_lazy("enterprise_list")
