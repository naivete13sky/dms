# Generated by Django 4.0.4 on 2022-07-30 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_manage', '0002_layer'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='layer_org',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1)], verbose_name='层名称'),
        ),
    ]
