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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role")
        self.register_by = kwargs.pop("register_by")
        roles = ()
        if role == "superadmin":
            roles = (
                ("superadmin", _("Super Admin")),
                ("admin", _("Administrator")),
            )

        elif role == "admin":
            roles = (
                ("visitador", _("Visitor")),
            )

        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = roles
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['document'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

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

class EditForm(forms.ModelForm):
    document = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=20, required=False)
    mobile = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "document", "phone", "mobile", "address", "email"]
        labels = {
            'first_name': _('Nombre(s)'),
            'last_name': _('Apellido(s'),
            'document': _('Documento'),
            'phone': _('Teléfono'),
            'mobile': _('Celular'),
            'address': _('Dirección'),
            'email': _('Correo Electrónico'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['document'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        profile = Profile.objects.get(user__username = user.username)
        user.first_name = self.check(user.first_name, "first_name")
        user.last_name = self.check(user.last_name, "last_name")
        user.email = self.check(user.email, "email")
        profile.document = self.check(profile.document, "document")
        profile.phone = self.check(profile.phone, "phone")
        profile.mobile = self.check(profile.mobile, "mobile")
        profile.address = self.check(profile.address, "address")

        if commit:
            user.save()
            profile.user = user
            profile.save()
        return user


    def check(self, property, data):
        data = self.cleaned_data[data]
        if data:
            return data
        else:
            return property

class DeactivateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("is_active", )

    def __init__(self, *args, **kwargs):
        super(DeactivateUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = _("Desmarque esta casilla si está seguro de que desea desactivar esta cuenta.")

    def save(self, commit=True):
        user = super(DeactivateUserForm, self).save(commit=False)
        profile = Profile.objects.get(user__username = user.username)
        user.is_active = self.cleaned_data["is_active"]

        if commit:
            user.save()
            profile.user = user
            profile.save()
        return user