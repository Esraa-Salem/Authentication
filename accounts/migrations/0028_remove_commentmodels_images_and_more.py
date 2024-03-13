# Generated by Django 4.2.2 on 2024-03-13 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_remove_request_username_request_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentmodels',
            name='images',
        ),
        migrations.RemoveField(
            model_name='commentmodels',
            name='username',
        ),
        migrations.AddField(
            model_name='commentmodels',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
