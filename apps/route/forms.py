from mongodbforms import DocumentForm
from .models import Route

class RouteForm(DocumentForm):
    class Meta:
        document = Route
        fields = ["name", "route"]