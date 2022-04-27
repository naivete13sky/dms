from django.db import models
from django.core import validators  # 自定义验证器
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from job_manage.models import Job

# Create your models here.
class ProjectManager(models.Manager):
    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(status ='published')


class Project(models.Model):
    # file_odb = models.FileField(upload_to='files', null=True,verbose_name="ODB++料号")
    # file_compressed = models.FileField(upload_to='files', null=True,verbose_name="原始料号压缩包")
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="工程名称")
    org=models.ForeignKey(Job, on_delete=models.CASCADE, related_name='project_job_org',verbose_name="原稿料号")
    work = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='project_job_work', verbose_name="工作稿料号")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="备注",blank=True)
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_user',verbose_name="负责人")

    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    last_update_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_last_user',null=True,blank=True,verbose_name="最后一次更新人")
    factory_rule_status = models.CharField(max_length=10, choices=(('no', '否'), ('yes', '是')), default='no',verbose_name="厂规")
    customer_rule_status = models.CharField(max_length=10, choices=(('no', '否'), ('yes', '是')), default='no',verbose_name="客规")
    create_type = models.CharField(max_length=10, choices=(('create', '创建'), ('share', '分享')), default='create',
                                            verbose_name="工程来源")


    objects = models.Manager()  # 默认的管理器
    published = ProjectManager()  # 自定义管理器
    tags=TaggableManager()

    class Meta:
        db_table = 'project'
        ordering = ('-publish',)

    # def get_absolute_url(self):
    #     return reverse('factoryruleformview', args=[self.id,])