# Generated by Django 3.1.3 on 2021-02-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0034_auto_20210211_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='count_reviews',
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='store_app.product', verbose_name='Товар'),
        ),
    ]
