# Generated by Django 3.0 on 2020-05-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0033_auto_20200527_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Reset', 'Reset'), ('Activation', 'Activation')], default='Activation', max_length=100),
        ),
    ]