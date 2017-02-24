from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from registration.backends.default.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegForm
from .models import User
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

class UsersListView(ListView):
    template_name = 'usermanage/userlist.html'

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return User.objects.all()

        elif self.request.user.groups.all()[0].name == "admin":
            return User.objects.filter(groups__name = "visitador")

        else:
            return User.objects.none()