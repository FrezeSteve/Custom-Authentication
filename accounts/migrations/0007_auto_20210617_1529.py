# Generated by Django 2.2.24 on 2021-06-17 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210617_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymoususer',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]