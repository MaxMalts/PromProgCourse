# Generated by Django 3.1.3 on 2020-11-04 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0004_auto_20201104_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)], verbose_name='Цена'),
        ),
    ]
