# Generated by Django 4.2.2 on 2024-02-29 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_addoffer_rent_finish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
