# Generated by Django 4.2.2 on 2024-03-13 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_commentmodels_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentmodels',
            name='requests',
        ),
    ]
