from django.views.generic import CreateView, UpdateView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from utils.decorators import require_service, require_login

# Create your views here.
class EventCreateView(CreateView):
    pass

class EventUpdateView(UpdateView):
    pass

class EventListView(ListView):
    pass
