# Generated by Django 3.0 on 2020-05-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0046_auto_20200530_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Activation', 'Activation'), ('Reset', 'Reset')], default='Activation', max_length=100),
        ),
    ]
