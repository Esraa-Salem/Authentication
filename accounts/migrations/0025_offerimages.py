# Generated by Django 4.2.2 on 2024-03-13 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_offermodels_area_offermodels_ava_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='offerImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='offer_images/')),
                ('offerimg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='accounts.offermodels')),
            ],
        ),
    ]
