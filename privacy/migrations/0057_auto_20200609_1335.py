# Generated by Django 3.0 on 2020-06-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0056_auto_20200609_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]
