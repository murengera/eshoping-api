# Generated by Django 3.0 on 2020-06-02 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0047_auto_20200530_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Reset', 'Reset'), ('Activation', 'Activation')], default='Activation', max_length=100),
        ),
    ]
