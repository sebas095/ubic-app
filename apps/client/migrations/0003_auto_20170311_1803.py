# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170308_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='client',
            name='lon',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='client',
            name='related_dir',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
