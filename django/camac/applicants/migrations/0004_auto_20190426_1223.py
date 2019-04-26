# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-26 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_auto_20190405_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='involved_applicants', to='instance.Instance'),
        ),
    ]
