# Generated by Django 4.0.4 on 2022-04-28 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_factoryrule_slug'),
        ('project', '0006_project_factory_rule_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_profile', to='account.profile', verbose_name='负责人'),
        ),
    ]
