# Generated by Django 3.0 on 2020-04-24 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0005_auto_20200424_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]
