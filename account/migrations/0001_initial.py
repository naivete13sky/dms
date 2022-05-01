# Generated by Django 4.0.4 on 2022-05-01 06:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='user/%Y/%m/%d/')),
                ('mobile', models.CharField(blank=True, max_length=11, validators=[django.core.validators.MinLengthValidator(limit_value=11)], verbose_name='手机号')),
                ('cam_level', models.CharField(blank=True, choices=[('level1', '等级1'), ('level2', '等级2'), ('level3', '等级3'), ('level4', '等级4'), ('level5', '等级5')], max_length=10, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recommender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_recommender', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='FactoryRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factory_rule_name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='厂规名称')),
                ('remark', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_factory_rule_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'db_table': 'factory_rule',
                'ordering': ('-publish',),
            },
        ),
    ]
