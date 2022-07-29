# Generated by Django 4.0.4 on 2022-07-29 08:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_odb', models.FileField(blank=True, null=True, upload_to='files', verbose_name='EP-ODB++')),
                ('file_compressed', models.FileField(blank=True, null=True, upload_to='files', verbose_name='原始文件')),
                ('file_org_type', models.CharField(choices=[('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'), ('odb++', 'ODB++'), ('else', '其它')], default='else', max_length=10, verbose_name='原始料号类型')),
                ('file_odb_current', models.FileField(blank=True, null=True, upload_to='files', verbose_name='最新-EP-ODB++')),
                ('file_odb_g', models.FileField(blank=True, null=True, upload_to='files', verbose_name='G-ODB++')),
                ('vs_result_ep', models.CharField(choices=[('success', '成功'), ('failed', '失败'), ('none', '未比对')], default='none', max_length=10, verbose_name='悦谱比图结果')),
                ('vs_result_g', models.CharField(choices=[('success', '成功'), ('failed', '失败'), ('none', '未比对')], default='none', max_length=10, verbose_name='G软件比图结果')),
                ('job_name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='料号名称')),
                ('job_type', models.CharField(choices=[('common', '普通板'), ('hdi', 'HDI'), ('led', 'LED板'), ('else', '其它')], default='common', max_length=10, verbose_name='料号类型')),
                ('remark', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('from_object', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=2)], verbose_name='料号来源')),
                ('publish', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='发布时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '正式')], default='draft', max_length=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_manage_jobs', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'db_table': 'job',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('password', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
                ('telephone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('1[3456789]\\d{9}', message='请输入正确的手机号码')])),
                ('email', models.CharField(max_length=20, validators=[django.core.validators.EmailValidator(message='请输入正确的邮箱地址')])),
            ],
            options={
                'db_table': 'register',
            },
        ),
        migrations.CreateModel(
            name='ShareAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('remark', models.CharField(blank=True, max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=3)], verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('share_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_manage_jobs_share_user', to=settings.AUTH_USER_MODEL, verbose_name='被分享人')),
                ('share_job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_manage_jobs_share_job', to='job_manage.job', verbose_name='被分享的料')),
            ],
            options={
                'ordering': ('share_job',),
            },
        ),
    ]
