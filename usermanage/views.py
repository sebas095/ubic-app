from django.views.generic import TemplateView, UpdateView, ListView
from registration.backends.default.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from .forms import RegForm, EditForm, DeactivateUserForm
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

class UserListView(ListView):
    template_name = 'usermanage/userlist.html'

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return User.objects.exclude(username=self.request.user.username)

        elif self.request.user.groups.all()[0].name == "admin":
            return User.objects.filter(profile__register_by__username = self.request.user.username)

        else:
            return User.objects.none()

class UserUpdateView(UpdateView):
    form_class = EditForm
    model = User
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('userlist')

class DeactivateAccountView(UpdateView):
    form_class = DeactivateUserForm
    model = User
    template_name = 'usermanage/deactivate_account.html'
    success_url = reverse_lazy('index')

