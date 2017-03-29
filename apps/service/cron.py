import django.core.mail
from .models import Service
from datetime import date

def scheduled_job():
    services = Service.objects.filter(is_active=True)
    for service in services:
        expiration_time = service.finish_date - date.today()
        if expiration_time.days == 7 or expiration_time.days == 1:
            email = service.enterprise.admin_by.email
            fullname = service.enterprise.admin_by.first_name + ' '
            fullname += service.enterprise.admin_by.last_name
            django.core.mail.send_mail(
                'Vencimiento del servicio',
                'Estimado usuario ' + fullname + \
                ',\n\nSe le informa que su servicio esta próximo a vencerse\n\nAtt,\nLa administración',
                'gefetic@gmail.com',
                [email],
                fail_silently=False,
            )
