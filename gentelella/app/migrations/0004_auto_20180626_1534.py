# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-26 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_sample_experiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='Release',
            field=models.CharField(default=2018, max_length=100),
        ),
    ]
