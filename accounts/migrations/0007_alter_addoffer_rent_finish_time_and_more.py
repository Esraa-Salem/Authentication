# Generated by Django 4.2.2 on 2024-02-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_offer_area_remove_offer_ava_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addoffer',
            name='rent_finish_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='addoffer',
            name='rent_start_time',
            field=models.DateTimeField(),
        ),
    ]
