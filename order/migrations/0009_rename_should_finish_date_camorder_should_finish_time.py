# Generated by Django 4.0.4 on 2022-05-07 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_camorder_should_finish_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camorder',
            old_name='should_finish_date',
            new_name='should_finish_time',
        ),
    ]