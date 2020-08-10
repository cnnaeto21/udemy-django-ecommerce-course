# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-27 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=120.0, max_digits=10),
        ),
    ]