# Generated by Django 3.0 on 2020-06-02 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0039_auto_20200602_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30),
        ),
    ]