# Generated by Django 3.0 on 2020-04-14 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPoliciesAndTermsOfUse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('language', models.CharField(choices=[('rwandese', 'rwandese'), ('english', 'english')], max_length=30)),
                ('_type', models.CharField(choices=[('terms_of_use', 'terms_of_use'), ('privacy_policy', 'privacy_policy')], max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Privacy Policies and Terms Of Use',
            },
        ),
    ]
