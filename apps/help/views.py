from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from .forms import HelpForm
from .models import Help

# Create your views here.
class HelpView(CreateView):
    model = Help
    form_class = HelpForm
    template_name = 'help_form.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['created_by']
            description = form.cleaned_data['description']
            send_mail(
                'Inquietud del usuario ' + user,
                'El usuario ' + user + ' informa lo siguiente:\n\n' + description,
                'gefetic@gmail.com',
                ['gefetic@gmail.com'],
            )

        return HttpResponseRedirect(self.success_url)