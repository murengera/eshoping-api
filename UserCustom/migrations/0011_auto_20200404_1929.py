# Generated by Django 3.0 on 2020-04-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0010_auto_20200402_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Reset', 'Reset'), ('Activation', 'Activation')], default='Activation', max_length=100),
        ),
    ]