# Generated by Django 2.2.24 on 2021-06-20 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210620_1608'),
        ('accounts', '0003_auto_20210620_1608'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnonymousUser',
        ),
        migrations.AddField(
            model_name='user',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to='accounts.DeviceTracker'),
        ),
    ]
