from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Route

class RouteSerializer(DocumentSerializer):

    class Meta:
        model = Route
        fields = '__all__'