from mongoengine import *
from django.utils.translation import ugettext as _

class Route(Document):
    name = StringField(help_text="")
    directions = StringField(help_text= _("Another"))
    clients = ListField(StringField(max_length=100))

    meta = {"db_alias": "secondary"}