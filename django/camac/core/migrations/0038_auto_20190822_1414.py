# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-22 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20190822_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationentry',
            name='type',
            field=models.ForeignKey(db_column='PUBLICATION_TYPE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.PublicationType'),
        ),
        migrations.AlterField(
            model_name='publicationsetting',
            name='type',
            field=models.ForeignKey(db_column='PUBLICATION_TYPE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.PublicationType'),
        ),
    ]
