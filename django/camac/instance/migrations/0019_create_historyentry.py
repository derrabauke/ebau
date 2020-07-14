# Generated by Django 2.2.13 on 2020-06-12 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import now

from camac.core.models import HistoryActionConfig


def migrate_journal(apps, schema_editor):
    Journal = apps.get_model("core.Journal")
    JournalT = apps.get_model("core.JournalT")
    JournalEntry = apps.get_model("instance.JournalEntry")
    HistoryEntry = apps.get_model("instance.HistoryEntry")
    HistoryEntryT = apps.get_model("instance.HistoryEntryT")

    for journal in Journal.objects.all():
        translations = JournalT.objects.filter(journal=journal)
        if journal.mode == "user":
            new_entry = JournalEntry.objects.create(
                instance=journal.instance,
                service=journal.service,
                user=journal.user,
                text=journal.text,
                creation_date=journal.created,
                modification_date=now(),
            )
            if translations:
                new_entry.text = translations[0].text
                new_entry.save()

        else:
            history_type = HistoryActionConfig.HISTORY_TYPE_STATUS
            if "Notifikation" in translations[0].text or "Notification" in translations[0].text:
                history_type = HistoryActionConfig.HISTORY_TYPE_NOTIFICATION

            new_entry = HistoryEntry.objects.create(
                instance=journal.instance,
                service=journal.service,
                user=journal.user,
                created_at=journal.created,
                title=journal.text,
                body=journal.additional_text,
                history_type=history_type,
            )
            for translation in translations:
                HistoryEntryT.objects.create(
                    title=translation.text,
                    body=translation.additional_text,
                    history_entry=new_entry,
                    language=translation.language,
                )



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0012_add_group_prefix"),
        ("instance", "0018_document_to_case"),
        ("core", "0043_journal_translation"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoryEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("title", models.TextField(blank=True, null=True)),
                ("body", models.TextField(blank=True, null=True)),
                ("history_type", models.CharField(max_length=20)),
                (
                    "instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="instance.Instance",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="user.Service",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="journalentry", name="duration"),
        migrations.RemoveField(model_name="journalentry", name="group"),
        migrations.AlterField(
            model_name="journalentry",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="HistoryEntryT",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("body", models.TextField(blank=True, null=True)),
                ("language", models.CharField(max_length=2)),
                (
                    "history_entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trans",
                        to="instance.HistoryEntry",
                    ),
                ),
            ],
        ),
        migrations.RunPython(migrate_journal),
        migrations.AlterField(
            model_name="historyentry",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]