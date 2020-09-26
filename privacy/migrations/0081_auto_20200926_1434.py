# Generated by Django 3.0 on 2020-09-26 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0080_auto_20200925_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='_type',
            field=models.CharField(choices=[('terms_of_use', 'terms_of_use'), ('privacy_policy', 'privacy_policy')], max_length=50),
        ),
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('rwandese', 'rwandese')], max_length=30),
        ),
    ]
