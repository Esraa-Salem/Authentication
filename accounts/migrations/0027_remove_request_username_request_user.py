# Generated by Django 4.2.2 on 2024-03-13 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_rename_image_offerimages_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='username',
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
