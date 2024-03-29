# Generated by Django 2.2.24 on 2021-06-20 13:08

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210618_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTracker',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('device_id', models.CharField(max_length=255, unique=True, verbose_name='Session ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_used', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'DeviceTracker',
                'verbose_name_plural': 'DeviceTracker',
                'ordering': ('-date_created',),
            },
        ),
        migrations.RemoveField(
            model_name='anonymoususer',
            name='user',
        ),
    ]
