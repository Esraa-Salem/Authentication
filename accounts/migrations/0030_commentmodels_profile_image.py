# Generated by Django 4.2.2 on 2024-03-13 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_alter_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodels',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='comment_image/'),
        ),
    ]
