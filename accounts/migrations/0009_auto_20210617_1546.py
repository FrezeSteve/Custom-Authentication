# Generated by Django 2.2.24 on 2021-06-17 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210617_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anonymoususer',
            name='date_updated',
        ),
        migrations.AddField(
            model_name='anonymoususer',
            name='last_used',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='anonymoususer',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='anonymoususer',
            name='session_id',
            field=models.CharField(editable=False, max_length=255, unique=True, verbose_name='Session ID'),
        ),
    ]