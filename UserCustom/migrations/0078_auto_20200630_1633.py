# Generated by Django 3.0 on 2020-06-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0077_auto_20200630_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='category',
            field=models.CharField(choices=[('Activation', 'Activation'), ('Reset', 'Reset')], default='Activation', max_length=100),
        ),
    ]