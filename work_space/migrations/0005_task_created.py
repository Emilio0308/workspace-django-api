# Generated by Django 4.2.4 on 2023-08-25 05:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('work_space', '0004_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]