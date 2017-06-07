from .models import Notification, Event
from django.http import HttpResponse
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .serializers import NotificationSerializer

# Create your views here.
class NotificationListAPI(GenericAPIView):
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'][4:]
        username = api_settings.JWT_DECODE_HANDLER(token)['username']
        notifications = Notification.objects(admin_by=username)
        notifications = list(map(self.filter, notifications))
        return HttpResponse(json.dumps(notifications), content_type='application/json')

    def filter(self, item):
        return {
            "id": str(item.id),
            "admin_by": item.admin_by,
            "event": {
                "created_by": item.event.created_by,
                "event_date": item.event.event_date,
                "type": item.event.type,
                "route": list(map(lambda r: r.name, item.event.route))
            }
        }


class NotificationCreateAPI(CreateAPIView):
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        event = Event.objects(id=request.POST['id'])
        admin_by = request.user.username

        if len(event) > 0:
            # TODO
            # send email
            # save with admin name
            event = event[0]
            data = {
                'event': event.id,
                'admin_by': admin_by
            }

            notification = NotificationSerializer(data=data)
            if notification.is_valid():
                notification.save()
                return Response({'ok': True}, status=status.HTTP_201_CREATED)
            return Response(notification.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class NotificationDeleteAPI(RetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = Event.objects(id=id)[0]
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)