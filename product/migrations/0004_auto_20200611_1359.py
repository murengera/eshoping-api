# Generated by Django 3.0 on 2020-06-11 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='item_condition',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
