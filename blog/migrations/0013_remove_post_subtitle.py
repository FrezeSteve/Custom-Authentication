# Generated by Django 2.2.24 on 2021-08-31 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210824_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='subtitle',
        ),
    ]
