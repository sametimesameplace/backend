# Generated by Django 4.2.6 on 2023-11-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timeplace", "0002_timeplace"),
    ]

    operations = [
        migrations.RenameField(
            model_name="timeplace",
            old_name="cleanup",
            new_name="deleted",
        ),
        migrations.AddField(
            model_name="timeplace",
            name="deleted_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
