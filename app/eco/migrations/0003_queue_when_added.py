# Generated by Django 5.1.2 on 2024-10-27 12:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0002_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='when_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]