# Generated by Django 3.0 on 2020-06-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0076_auto_20200630_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='_type',
            field=models.CharField(choices=[('privacy_policy', 'privacy_policy'), ('terms_of_use', 'terms_of_use')], max_length=50),
        ),
    ]