from mongoengine import *
from django.utils.translation import ugettext as _
from apps.route.models import Route

# Create your models here.
class Event(Document):
    created_by = StringField(help_text='')
    event_date = DateTimeField()
    description = StringField(help_text='')
    type = StringField(help_text='')
    route = ListField(ReferenceField(Route))

    meta = {"db_alias": "secondary"}

    def __str__(self):
        return self.type

class Loan(Document):
    created_by = StringField(help_text='')
    total_amount = FloatField(min_value=0.0)
    payment_fee = IntField(min_value=0)
    rate = FloatField(min_value=0.0)
    collection = FloatField(min_value=0.0)
    event = ReferenceField(Event, null=True)

    meta = {"db_alias": "secondary"}

# TODO
# Un modelo que se llame prestamo
# Monto total
# Cuotas
# Tasa
# Recaudado
# Incluya una relacion hacia el evento Que puede ser null