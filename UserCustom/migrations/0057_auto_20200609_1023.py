# Generated by Django 3.0 on 2020-06-09 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0056_auto_20200609_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Activation', 'Activation'), ('Reset', 'Reset')], default='Activation', max_length=100),
        ),
    ]
