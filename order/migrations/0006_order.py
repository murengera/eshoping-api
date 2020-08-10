# Generated by Django 3.0 on 2020-06-11 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0007_productreviewers_product'),
        ('order', '0005_auto_20200611_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_code', models.CharField(blank=True, editable=False, max_length=18)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('finished_at', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('ACTIVE', 'ACTIVE'), ('FINISHED', 'FINISHED')], default='NEW', max_length=50)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.Producte')),
            ],
        ),
    ]