# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-31 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('orders', '0003_auto_20190830_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.Address'),
        ),
    ]
