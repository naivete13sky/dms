# Generated by Django 4.0.4 on 2022-05-01 06:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('job_manage', '0005_remove_itemimage_item_delete_item_delete_itemimage'),
    ]

    operations = [
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_factory_rule_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'db_table': 'project_factory_rule',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='工程名称')),
                ('remark', models.CharField(blank=True, max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('factory_rule_status', models.CharField(blank=True, choices=[('no', '否'), ('yes', '是')], default='no', max_length=10, null=True, verbose_name='厂规状态')),
                ('customer_rule_status', models.CharField(blank=True, choices=[('no', '否'), ('yes', '是')], default='no', max_length=10, null=True, verbose_name='客规状态')),
                ('create_type', models.CharField(choices=[('create', '创建'), ('share', '分享')], default='create', max_length=10, verbose_name='工程来源')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_user', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
                ('factory_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_factory_rule', to='project.factoryrule', verbose_name='厂规')),
                ('last_update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_last_user', to=settings.AUTH_USER_MODEL, verbose_name='最后一次更新人')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_job_org', to='job_manage.job', verbose_name='原稿料号')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_job_work', to='job_manage.job', verbose_name='工作稿料号')),
            ],
            options={
                'db_table': 'project',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='CustomerRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_rule_name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='客规名称')),
                ('remark', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_customer_rule_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'db_table': 'project_customer_rule',
                'ordering': ('-publish',),
            },
        ),
    ]
