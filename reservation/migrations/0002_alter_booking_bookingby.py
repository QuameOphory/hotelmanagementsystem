# Generated by Django 4.0.5 on 2022-06-17 13:23

from django.conf import settings
import django.contrib.auth
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bookingby',
            field=models.ForeignKey(default=django.contrib.auth.get_user_model, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
    ]