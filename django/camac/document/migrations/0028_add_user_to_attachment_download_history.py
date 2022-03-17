# Generated by Django 2.2.17 on 2022-02-22 09:23

from logging import getLogger
from django.conf import settings
from django.db import migrations, models
from django.db.models import OuterRef, Subquery
import django.db.models.deletion

log = getLogger()


def set_user(apps, schema_editor):
    AttachmentDownloadHistory = apps.get_model("document", "AttachmentDownloadHistory")
    User = apps.get_model("user", "User")

    AttachmentDownloadHistory.objects.update(
        user_id=Subquery(
            User.objects.filter(username=OuterRef("keycloak_id")).values("pk")[:1]
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("document", "0027_remove_section_acls"),
    ]

    operations = [
        migrations.AddField(
            model_name="attachmentdownloadhistory",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attachment_download_history",
                null=True,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.RunPython(set_user, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="attachmentdownloadhistory",
            name="keycloak_id",
        ),
        migrations.RemoveField(
            model_name="attachmentdownloadhistory",
            name="name",
        ),
    ]
