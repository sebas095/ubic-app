from django.db import models
from apps.enterprise.models import Enterprise
from apps.usermanage.models import User

# Create your models here.
class Service(models.Model):
    enterprise = models.OneToOneField(Enterprise)
    start_date = models.DateField()
    finish_date = models.DateField()
    type = models.CharField(max_length=100)
    rate = models.FloatField()
    observations = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type