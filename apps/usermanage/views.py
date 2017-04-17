from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, ListView, View
from registration.backends.default.views import RegistrationView
from django.core.urlresolvers import reverse_lazy
from .forms import RegForm, EditForm, DeactivateUserForm
from .models import User
from apps.service.models import Service
from utils.decorators import require_service, require_login
from datetime import date

# Create your views here.
@require_login
@require_service
class RegView(RegistrationView):
    form_class = RegForm

    def get_form_kwargs(self):
        kwargs = super(RegView, self).get_form_kwargs()
        kwargs.update({"role": self.request.user.groups.all()[0].name})
        kwargs.update({"register_by": self.request.user})
        return kwargs


class HomePageView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.user.groups.all()[0].name == "admin":
                if Service.objects.filter(enterprise__admin_by__username=request.user.username):
                    service = Service.objects.filter(enterprise__admin_by__username=request.user.username)[0]
                    expiration_time = service.finish_date - date.today()
                    if expiration_time.days <= 7:
                        return render(request, 'index.html', {
                            "msg": "Su servicio esta próximo a vencerse"
                        })
                    else:
                        return render(request, 'index.html')
                else:
                    return render(request, 'index.html')
            else:
                return render(request, 'index.html')
        else:
            return render(request, 'index.html')

@require_login
@require_service
class UserListView(ListView):
    template_name = "userlist.html"

    def get_queryset(self):
        if self.request.user.groups.all()[0].name == "superadmin":
            return User.objects.exclude(username=self.request.user.username)

        elif self.request.user.groups.all()[0].name == "admin":
            return User.objects.filter(profile__register_by__username = self.request.user.username)

        else:
            return User.objects.none()

@require_login
@require_service
class UserUpdateView(UpdateView):
    form_class = EditForm
    model = User
    template_name = "user_registration_form.html"
    success_url = reverse_lazy("userlist")

@require_login
@require_service
class DeactivateAccountView(UpdateView):
    form_class = DeactivateUserForm
    model = User
    template_name = "deactivate_account.html"
    success_url = reverse_lazy("userlist")

    def post(self, request, *args, **kwargs):
        user = self.model.objects.get(id=kwargs["pk"])
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
        if not form.cleaned_data["is_active"] and not self.request.user.id:
            self.success_url = reverse_lazy("index")
        return HttpResponseRedirect(self.get_success_url())
