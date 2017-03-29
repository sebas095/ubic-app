from django.db import models

# Create your models here.
class Event(models.Model):
    #services
    created_by = models.CharField(max_length=100)
    event_date = models.DateField()