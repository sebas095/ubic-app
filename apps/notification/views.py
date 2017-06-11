from .models import Notification, Event
from django.http import HttpResponse
import django.core.mail
from apps.usermanage.models import Profile, User
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .serializers import NotificationSerializer

# Create your views here.
class NotificationCountAPI(GenericAPIView):
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notifications = Notification.objects(admin_by=request.user.username)
        return HttpResponse(json.dumps(len(notifications)), content_type='application/json')

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
                "description": item.event.description,
                "event_date": str(item.event.event_date),
                "type": item.event.type,
                "routes": list(map(lambda r: r.name, item.event.route))
            }
        }


class NotificationCreateAPI(CreateAPIView):
    lookup_field = 'id'
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        event = Event.objects(id=request.POST['id'])
        email = ""
        fullname = ""

        if len(event) > 0:
            admin_by = Profile.objects.filter(user__username=request.user.username)[0].register_by
            if admin_by:
                fullname = admin_by.first_name + " " + admin_by.last_name
                email = admin_by.email
                admin_by = admin_by.username
            else:
                admin_by = User.objects.filter(username=request.user.username)[0]
                fullname = admin_by.first_name + " " + admin_by.last_name
                email = admin_by.email
                admin_by = admin_by.username

            event = event[0]
            routes = list(map(lambda r: r.name, event.route))
            django.core.mail.send_mail(
                'Notificación UbicApp',
                '',
                'gefetic@gmail.com',
                [email],
                html_message='Estimado usuario ' + fullname + \
                    ',<br><br>Se le informa que el usuario ' + request.user.username + \
                    ' ha creado un evento con la siguiente información:<br>' + \
                    '<ul><li><b>Fecha del evento: </b>' + str(event.event_date) + '</li>' + \
                    '<li><b>Descripción: </b>' + event.description + '</li>' + \
                    '<li><b>Tipo: </b>' + event.type + '</li>' + \
                    '<li><b>Ruta(s): </b>' + ", ".join(routes) + '</li></ul>' + \
                    '<br><br>Atte,<br>La administración',
                fail_silently=False,
            )

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
        notif = Notification.objects(id=id)[0]
        notif.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)