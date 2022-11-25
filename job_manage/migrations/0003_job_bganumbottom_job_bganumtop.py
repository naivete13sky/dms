# Generated by Django 4.0.4 on 2022-10-28 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_manage', '0002_job_minlinespace4outerbottom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='bgaNumBottom',
            field=models.IntegerField(blank=True, help_text='背面BGA总数', null=True, validators=[django.core.validators.MaxValueValidator(100000000), django.core.validators.MinValueValidator(0)], verbose_name='背面BGA总数'),
        ),
        migrations.AddField(
            model_name='job',
            name='bgaNumTop',
            field=models.IntegerField(blank=True, help_text='正面BGA总数', null=True, validators=[django.core.validators.MaxValueValidator(100000000), django.core.validators.MinValueValidator(0)], verbose_name='正面BGA总数'),
        ),
    ]