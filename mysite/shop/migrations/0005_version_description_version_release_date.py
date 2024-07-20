# Generated by Django 5.0.7 on 2024-07-20 10:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='description',
            field=models.TextField(default='Описание по умолчанию'),
        ),
        migrations.AddField(
            model_name='version',
            name='release_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
