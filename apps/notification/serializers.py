from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Notification

class NotificationSerializer(DocumentSerializer):

    class Meta:
        model = Notification
        fields = '__all__'