# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-07-28 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20200529_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_digital',
            field=models.BooleanField(default=False),
        ),
    ]
