from django.views.generic import CreateView, UpdateView, ListView
from .forms import EnterpriseForm
from.models import Enterprise

# Create your views here.
class EnterpriseCreateView(CreateView):
    form_class = EnterpriseForm
    model = Enterprise
    template_name = "registration/registration_form.html"