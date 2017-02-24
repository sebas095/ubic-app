from registration.forms import RegistrationForm
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group
from django import forms
from .models import Profile

class RegForm(RegistrationForm):

    required_css_class = 'required'
    document = forms.CharField(label=_("Document"), max_length=20, required=True)
    phone = forms.CharField(max_length=20, required=True)
    mobile = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(choices=())
    register_by = ""

    class Meta:
        model = User
        fields = ("username", "role", "first_name", "last_name", "document", "phone", "mobile", "address", "email")

    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role")
        self.register_by = kwargs.pop("register_by")
        roles = ()
        if role == "superadmin":
            roles = (
                ("superadmin", _("Super Admin")),
                ("admin", _("Administrator"))
            )

        elif role == "admin":
            roles = (
                ("visitador", "visitador")
            )

        super(RegForm,self).__init__(*args, **kwargs)
        self.fields['role'].choices = roles

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        profile = Profile()
        profile.document = self.cleaned_data["document"]
        profile.phone = self.cleaned_data["phone"]
        profile.mobile = self.cleaned_data["mobile"]
        profile.address = self.cleaned_data["address"]
        profile.register_by = self.register_by

        if commit:
            user.save()
            g = Group.objects.get(name=self.cleaned_data["role"])
            g.user_set.add(user)
            profile.user = user
            profile.save()
        return user