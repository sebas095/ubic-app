from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from .forms import EnterpriseForm, EnterpriseEditForm, DeactiveEnterpriseForm
from.models import Enterprise
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.decorators import require_service

# Create your views here.
@require_service
class EnterpriseCreateView(CreateView):
    form_class = EnterpriseForm
    model = Enterprise
    template_name = "enterprise_form.html"
    success_url = reverse_lazy("enterprise_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnterpriseCreateView, self).dispatch(*args, **kwargs)

@require_service
class EnterpriseUpdateView(UpdateView):
    form_class = EnterpriseEditForm
    model = Enterprise
    template_name = "enterprise_edit_form.html"
    success_url = reverse_lazy("enterprise_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnterpriseUpdateView, self).dispatch(*args, **kwargs)

@require_service
class EnterpriseListView(ListView):
    template_name = "enterpriselist.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnterpriseListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return Enterprise.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return Enterprise.objects.filter(is_active=True)

        else:
            return Enterprise.objects.none()

@require_service
class EnterpriseDeactivateView(UpdateView):
    form_class = DeactiveEnterpriseForm
    model = Enterprise
    template_name = "deactivate_enterprise_account.html"
    success_url = reverse_lazy("enterprise_list")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnterpriseDeactivateView, self).dispatch(*args, **kwargs)
