# Generated by Django 4.0.4 on 2022-04-27 02:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_project_create_type_alter_project_create_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
    ]
