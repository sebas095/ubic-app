from mongoengine import *
from django.utils.translation import ugettext as _
from apps.event.models import Event

# Create your models here.
class Notification(Document):
    event = ReferenceField(Event)
    admin_by = StringField(help_text="")

    meta = {"db_alias": "secondary"}

