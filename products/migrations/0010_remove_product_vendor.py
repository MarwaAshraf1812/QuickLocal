# Generated by Django 4.2 on 2024-07-24 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]
