# Generated by Django 3.0 on 2020-06-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0048_auto_20200609_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='_type',
            field=models.CharField(choices=[('privacy_policy', 'privacy_policy'), ('terms_of_use', 'terms_of_use')], max_length=50),
        ),
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('rwandese', 'rwandese')], max_length=30),
        ),
    ]
