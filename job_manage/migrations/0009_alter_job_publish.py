# Generated by Django 4.0.4 on 2022-05-07 09:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_manage', '0008_alter_job_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='publish',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
