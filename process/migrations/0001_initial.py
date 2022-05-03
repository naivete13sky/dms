# Generated by Django 4.0.4 on 2022-05-03 17:07

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
            name='Carriage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='车厢名称')),
                ('remark', models.CharField(blank=True, max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('carriage_type', models.CharField(blank=True, choices=[('head', '车头'), ('mid', '中间'), ('tail', '车尾')], default='head', max_length=10, null=True, verbose_name='车厢类型')),
                ('carriage_use', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='车厢用途')),
                ('check_set', models.CharField(blank=True, choices=[('no', '无需审核'), ('yes', '需要审核')], default='no', max_length=10, null=True, verbose_name='是否需要审核')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author_check', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='process_carriage_author_check_user', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
                ('author_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='process_carriage_author_create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('author_exe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='process_carriage_author_exe_user', to=settings.AUTH_USER_MODEL, verbose_name='执行人')),
            ],
            options={
                'db_table': 'process_carriage',
                'ordering': ('-publish',),
            },
        ),
    ]
