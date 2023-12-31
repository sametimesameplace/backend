# Generated by Django 4.2.7 on 2023-11-15 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeplace', '0005_rename_user_id_timeplace_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('email_user_1', models.BooleanField()),
                ('email_user_2', models.BooleanField()),
                ('phone_user_1', models.BooleanField()),
                ('phone_user_2', models.BooleanField()),
                ('chat_accepted', models.BooleanField()),
                ('timeplace_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeplace_1', to='timeplace.timeplace')),
                ('timeplace_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeplace_2', to='timeplace.timeplace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MatchChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(max_length=500)),
                ('match_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.match')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
