from mongoengine import *
from django.utils.translation import ugettext as _

class Route(Document):
    name = StringField(help_text="")
    directions = StringField(help_text= _("Another"))
    clients = ListField(IntField())

    meta = {"db_alias": "secondary"}