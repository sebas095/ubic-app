from mongoengine import *
from django.utils.translation import ugettext as _
from datetime import datetime

class Route(Document):
    enterprise = StringField(help_text="")
    created_at = DateTimeField(default=datetime.now)
    name = StringField(help_text="")
    directions = StringField(help_text= _("Another"))
    clients = ListField(IntField())

    meta = {"db_alias": "secondary"}

    def __str__(self):
        return self.name