# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-23 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
