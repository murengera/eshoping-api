# Generated by Django 3.0 on 2020-06-08 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0054_auto_20200608_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Activation', 'Activation'), ('Reset', 'Reset')], default='Activation', max_length=100),
        ),
    ]
