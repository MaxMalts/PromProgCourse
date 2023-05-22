# Generated by Django 3.1.3 on 2020-11-24 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0011_auto_20201123_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Оценка'),
        ),
    ]
