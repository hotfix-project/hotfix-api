# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-05 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170805_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patch',
            name='remote_url',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]