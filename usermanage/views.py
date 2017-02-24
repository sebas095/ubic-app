from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from registration.backends.default.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegForm, RutasForm

# Create your views here.

class RegView(RegistrationView):
    form_class = RegForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(RegView,self).get_form_kwargs()
        kwargs.update({"role": self.request.user.groups.all()[0].name})
        kwargs.update({"register_by": self.request.user})
        return kwargs

class HomePageView(TemplateView):
    template_name = "index.html"

class CreateRuta(CreateView):
    form_class = RutasForm
    template_name = "ruta.html"