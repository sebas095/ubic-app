from mongoengine import *
from django.utils.translation import ugettext as _

class Route(Document):
    name = StringField(help_text = _("Define a name for the route"))
    route = StringField(help_text = _("Another"))

    meta = {"db_alias": "secondary"}