# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-07-25 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200613_0214'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='key',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
