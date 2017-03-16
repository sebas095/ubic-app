from mongoengine import Document, fields

class Route(Document):
    name = fields.StringField()
    route = fields.StringField()