# Generated by Django 3.0 on 2020-06-11 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_producte'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreviewers',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Producte'),
        ),
    ]
