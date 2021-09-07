# Generated by Django 2.2.17 on 2021-09-07 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0026_auto_20210413_1850'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attachmentsectionroleacl',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='attachmentsectionroleacl',
            name='attachment_section',
        ),
        migrations.RemoveField(
            model_name='attachmentsectionroleacl',
            name='role',
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectionserviceacl',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='attachmentsectionserviceacl',
            name='attachment_section',
        ),
        migrations.RemoveField(
            model_name='attachmentsectionserviceacl',
            name='service',
        ),
        migrations.DeleteModel(
            name='AttachmentSectionGroupAcl',
        ),
        migrations.DeleteModel(
            name='AttachmentSectionRoleAcl',
        ),
        migrations.DeleteModel(
            name='AttachmentSectionServiceAcl',
        ),
    ]
