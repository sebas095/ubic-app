from django.db import models
from apps.enterprise.models import Enterprise

# Create your models here.
class Client(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    fullname = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    observations = models.TextField(null=True)