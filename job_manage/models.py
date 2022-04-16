# Create your models here.
from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Job(models.Model):
    file_odb = models.FileField(upload_to='router_job_odb', verbose_name="ODB++(.tgz)")
    file_compressed = models.FileField(upload_to='router_job_compressed', verbose_name="原始资料（压缩包）")
    RECIPE_STATUS_CHOICES = (('yes', 'yes'), ('no', 'no'))

    job_name = models.CharField(max_length=250,verbose_name="料号名称")
    slug = models.SlugField(max_length=250, unique_for_date='receive_date')
    receive_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='use_org',verbose_name="料号负责人")
    receive_date = models.DateTimeField(default=timezone.now,verbose_name="接受料号时间")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipe_status = models.CharField(max_length=10, choices=RECIPE_STATUS_CHOICES, default='no',verbose_name="是否提供了参数")
    remark = models.TextField(verbose_name="备注")

    class Meta:
        ordering = ('-receive_date',)
        verbose_name = '料号'
        verbose_name_plural = '料号'

    def __str__(self):
        return self.job_name


from django.db import models

# 自定义验证器
from django.core import validators
class Article(models.Model):
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器
    # MinLengthValidator
    title = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)])
    content = models.TextField(max_length=100, validators=[validators.MinLengthValidator(limit_value=3)])
    author = models.CharField(max_length=15)
    create_time = models.DateTimeField(auto_now_add=True)

    # FileField 为文件上传功能
    # upload_to:对应的files创建的文件夹目录
    images = models.FileField(upload_to='files', null=True)
    # images = models.FileField(upload_to='%Y/%M/%D', null=True)

    class Meta:
        db_table = 'article'

class Register(models.Model):
    # 当不能设置最小长度的时候,可以使用自定义验证器来弄最小长度值
    # 对应的字段里面都会对应的自定义验证器使用
    username = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    password = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    telephone = models.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='请输入正确的手机号码')])
    email = models.CharField(max_length=20, validators=[validators.EmailValidator(message='请输入正确的邮箱地址')])

    class Meta:
        db_table = 'register'

