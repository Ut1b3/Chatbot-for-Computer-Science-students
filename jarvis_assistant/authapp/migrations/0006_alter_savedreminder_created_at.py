# Generated by Django 5.0.6 on 2024-06-12 12:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_savedreminder_created_at_savedreminder_due_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedreminder',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
