from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=50, null=True)
    register_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.user.username