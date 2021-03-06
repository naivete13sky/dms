# Generated by Django 4.0.4 on 2022-07-29 08:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(limit_value=1)], verbose_name='层名称')),
                ('layer_file_type', models.CharField(choices=[('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'), ('excellon2', 'Excellon2'), ('excellon1', 'Excellon1'), ('dxf', 'DXF'), ('else', '其它')], default='else', max_length=10, verbose_name='层文件类型')),
                ('layer_type', models.CharField(choices=[('signal_outter', '外层'), ('signal_inner', '内层'), ('solder', '防焊'), ('silk', '丝印'), ('paste', '锡膏'), ('drill', '孔层'), ('rout', 'Rout'), ('slot', '槽孔'), ('else', '其它')], default='else', max_length=20, verbose_name='层类型')),
                ('features_count', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100000000), django.core.validators.MinValueValidator(0)], verbose_name='物件数')),
                ('drill_excellon2_units', models.CharField(choices=[('Inch', 'Inch'), ('MM', 'MM'), ('none', '未记录')], default='none', max_length=10, verbose_name='E2_units')),
                ('drill_excellon2_zeroes_omitted', models.CharField(choices=[('Leading', 'Leading'), ('Trailing', 'Trailing'), ('none', '未记录')], default='none', max_length=10, verbose_name='E2省零')),
                ('drill_excellon2_number_format_A', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')], default='none', max_length=10, verbose_name='E2_format_A')),
                ('drill_excellon2_number_format_B', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')], default='none', max_length=10, verbose_name='E2_format_B')),
                ('drill_excellon2_tool_units', models.CharField(choices=[('Inch', 'Inch'), ('MM', 'MM'), ('Mils', 'Mils'), ('none', '未记录')], default='none', max_length=10, verbose_name='E2_tool')),
                ('remark', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=1)], verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_manage_layer_user', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_manage_layer', to='job_manage.job', verbose_name='料号名称')),
            ],
            options={
                'db_table': 'layer',
                'ordering': ('-create_time',),
            },
        ),
    ]
