from mongodbforms import DocumentForm
from .models import Route

class RouteForm(DocumentForm):

    class Meta:
        pass
        #document = Route
        #fields = ['name', 'route']