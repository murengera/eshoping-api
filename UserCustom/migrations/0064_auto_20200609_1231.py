# Generated by Django 3.0 on 2020-06-09 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0063_auto_20200609_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Reset', 'Reset'), ('Activation', 'Activation')], default='Activation', max_length=100),
        ),
    ]
