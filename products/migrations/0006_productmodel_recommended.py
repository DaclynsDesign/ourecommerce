# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-24 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20190824_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='recommended',
            field=models.BooleanField(default=False),
        ),
    ]
