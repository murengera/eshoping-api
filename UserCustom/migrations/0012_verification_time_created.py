# Generated by Django 3.0 on 2020-04-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserCustom', '0011_auto_20200404_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='time_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
