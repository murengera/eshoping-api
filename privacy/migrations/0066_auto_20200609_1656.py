# Generated by Django 3.0 on 2020-06-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0065_auto_20200609_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('rwandese', 'rwandese')], max_length=30),
        ),
    ]