# Generated by Django 3.0 on 2020-04-28 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0013_auto_20200429_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]
