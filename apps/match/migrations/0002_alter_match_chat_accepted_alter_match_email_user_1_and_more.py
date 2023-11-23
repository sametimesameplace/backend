# Generated by Django 4.2.7 on 2023-11-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("match", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="chat_accepted",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="match",
            name="email_user_1",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="match",
            name="email_user_2",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="match",
            name="phone_user_1",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="match",
            name="phone_user_2",
            field=models.BooleanField(default=False),
        ),
    ]
