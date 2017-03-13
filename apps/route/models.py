from mongoengine import *

class Route(Document):
    name = fields.StringField()
    route = fields.StringField()