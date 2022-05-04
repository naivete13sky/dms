# Create your models here.
from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core import validators  # 自定义验证器
from django.urls import reverse
from taggit.managers import TaggableManager

class JobManager(models.Manager):
    def get_queryset(self):
        return super(JobManager, self).get_queryset().filter(status ='published')
        # return super(JobManager, self).get_queryset().all()

class Job(models.Model):
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器
    # MinLengthValidator
    # FileField 为文件上传功能
    # upload_to:对应的files创建的文件夹目录
    # images = models.FileField(upload_to='%Y/%M/%D', null=True)
    file_odb = models.FileField(upload_to='files',blank=True, null=True,verbose_name="ODB++料号")
    file_compressed = models.FileField(upload_to='files',blank=True, null=True,verbose_name="原始料号压缩包")
    job_name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="料号名称")
    # remark = models.TextField(max_length=100, validators=[validators.MinLengthValidator(limit_value=3)])
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="备注",blank=True)
    # slug = models.SlugField(max_length=250, unique_for_date='publish')

    # author = models.CharField(max_length=15)
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_jobs',null=True,blank=True,verbose_name="负责人")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # 默认的管理器
    published = JobManager()  # 自定义管理器
    tags=TaggableManager()

    class Meta:
        db_table = 'job'
        ordering = ('-publish',)
    # def get_absolute_url(self):
    #     return reverse('job_manage:job_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    def get_absolute_url(self):
        return reverse('job_manage:JobFormView', args=[self.id, ])
        # return reverse('job_manage:job_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    def __str__(self):
        # Return a string that represents the instance
        return self.job_name

class Register(models.Model):
    # 当不能设置最小长度的时候,可以使用自定义验证器来弄最小长度值
    # 对应的字段里面都会对应的自定义验证器使用
    username = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    password = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=3)])
    telephone = models.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456789]\d{9}', message='请输入正确的手机号码')])
    email = models.CharField(max_length=20, validators=[validators.EmailValidator(message='请输入正确的邮箱地址')])
    class Meta:
        db_table = 'register'

class ShareAccount(models.Model):
    pass
    share_job=models.ForeignKey(Job, on_delete=models.DO_NOTHING,related_name='job_manage_jobs_share_job',verbose_name="被分享的料")
    share_account=models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_jobs_share_user',verbose_name="被分享人")
    publish = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注",blank=True)
    # slug = models.SlugField(max_length=250, unique_for_date='publish')
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=("share_job",)



