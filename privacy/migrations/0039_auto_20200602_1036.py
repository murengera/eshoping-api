# Generated by Django 3.0 on 2020-06-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy', '0038_auto_20200602_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypoliciesandtermsofuse',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('rwandese', 'rwandese')], max_length=30),
        ),
    ]