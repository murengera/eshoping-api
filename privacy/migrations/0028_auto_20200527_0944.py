# Generated by Django 3.0 on 2020-05-27 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0027_auto_20200527_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]
