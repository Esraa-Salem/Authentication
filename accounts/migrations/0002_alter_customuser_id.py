# Generated by Django 4.2.2 on 2024-01-22 19:05

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefhgigklmnoqz93801 ', length=10, max_length=20, prefix='rest', primary_key=True, serialize=False, unique=True),
        ),
    ]
