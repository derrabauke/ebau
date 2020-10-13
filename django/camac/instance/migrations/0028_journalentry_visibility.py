# Generated by Django 2.2.14 on 2020-08-19 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0027_fix_ech_circulations'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='visibility',
            field=models.CharField(choices=[('all', 'All'), ('own_organization', 'Own Organization'), ('authorities', 'Authorities')], default='own_organization', max_length=16),
        ),
    ]
