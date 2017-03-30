from mongoengine import *
from django.utils.translation import ugettext as _

# Create your models here.
class Event(Document):
    created_by = StringField(help_text='')
    event_date = DateTimeField()
    description = StringField(help_text='')
    type = StringField(help_text='')
    route_id = StringField(help_text='')

    meta = {"db_alias": "secondary"}
