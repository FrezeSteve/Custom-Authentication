# Generated by Django 2.2.24 on 2021-06-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210617_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymoususer',
            name='session_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='Session ID'),
        ),
    ]
