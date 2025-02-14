from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _

from apps.usermanage.models import User

# Create your models here.
class Enterprise(models.Model):
    nit = models.CharField(max_length=16, unique=True)
    social_respon = models.TextField(max_length=500, null=True, verbose_name=_("Social responsibility"))
    address = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    admin_by = models.OneToOneField(User)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.social_respon