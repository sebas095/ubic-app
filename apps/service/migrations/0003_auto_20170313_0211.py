# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_service_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='admin_by',
        ),
        migrations.AlterField(
            model_name='service',
            name='finish_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='start_date',
            field=models.DateField(),
        ),
    ]
