# Generated by Django 4.0.4 on 2022-05-04 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_camorder_name_alter_camorder_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camorderprocess',
            name='data',
            field=models.JSONField(blank=True, db_index=True, null=True),
        ),
    ]