from django.db import models
from datetime import datetime

# Create your models here.
class Help(models.Model):
    created_by = models.CharField(null=False, max_length=100)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(default=datetime.now)