# Generated by Django 3.2.12 on 2022-03-01 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0033_journalentry_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='value',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='historyentry',
            name='history_type',
            field=models.CharField(choices=[], max_length=20),
        ),
    ]