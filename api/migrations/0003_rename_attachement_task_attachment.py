# Generated by Django 3.2.5 on 2021-07-19 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_task_attachement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='attachement',
            new_name='attachment',
        ),
    ]
