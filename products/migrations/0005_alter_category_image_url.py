# Generated by Django 3.2.6 on 2021-09-06 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image_url',
            field=models.URLField(max_length=1000),
        ),
    ]