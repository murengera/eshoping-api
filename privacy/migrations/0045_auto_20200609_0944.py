# Generated by Django 3.0 on 2020-06-09 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0044_auto_20200608_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='_type',
            field=models.CharField(choices=[('terms_of_use', 'terms_of_use'), ('privacy_policy', 'privacy_policy')], max_length=50),
        ),
    ]
