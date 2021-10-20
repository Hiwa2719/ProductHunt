# Generated by Django 3.2.8 on 2021-10-19 19:37

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20211019_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='icon',
            field=models.ImageField(blank=True, upload_to=products.models.icon_field_upload_location),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=products.models.image_field_upload_location),
        ),
    ]