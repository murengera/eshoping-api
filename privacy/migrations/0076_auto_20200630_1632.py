# Generated by Django 3.0 on 2020-06-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0075_auto_20200630_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]