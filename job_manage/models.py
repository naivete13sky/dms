# Create your models here.
from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
# 自定义验证器
from django.core import validators

class Job(models.Model):
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器
    # MinLengthValidator
    # FileField 为文件上传功能
    # upload_to:对应的files创建的文件夹目录
    # images = models.FileField(upload_to='%Y/%M/%D', null=True)
    file_odb = models.FileField(upload_to='files', null=True)
    file_compressed = models.FileField(upload_to='files', null=True)
    job_name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)])
    remark = models.TextField(max_length=100, validators=[validators.MinLengthValidator(limit_value=3)])
    author = models.CharField(max_length=15)
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'job'

class Register(models.Model):
    # 当不能设置最小长度的时候,可以使用自定义验证器来弄最小长度值
    # 对应的字段里面都会对应的自定义验证器使用
    username = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    password = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    telephone = models.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='请输入正确的手机号码')])
    email = models.CharField(max_length=20, validators=[validators.EmailValidator(message='请输入正确的邮箱地址')])

    class Meta:
        db_table = 'register'
