# Generated by Django 4.2 on 2024-07-24 21:20

from django.db import migrations, models
import vendor.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_product_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=vendor.models.Vendor),
        ),
    ]