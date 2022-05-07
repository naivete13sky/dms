from django.db import models
from django.core import validators  # 自定义验证器
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
import project
from job_manage.models import Job
from account.models import Profile



# Create your models here.
class ProjectManager(models.Manager):
    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(status ='published')


class Project(models.Model):
    # file_odb = models.FileField(upload_to='files', null=True,verbose_name="ODB++料号")
    # file_compressed = models.FileField(upload_to='files', null=True,verbose_name="原始料号压缩包")
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="工程名称")
    org=models.ForeignKey(Job, on_delete=models.CASCADE, related_name='project_job_org',verbose_name="原稿料号")
    work = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='project_job_work',blank=True,null=True, verbose_name="工作稿料号")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="备注",blank=True)
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_user',verbose_name="负责人")
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_profile', verbose_name="负责人")

    publish = models.DateTimeField(default=timezone.now,verbose_name="发布时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")


    last_update_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_last_user',null=True,blank=True,verbose_name="最后一次更新人")
    factory_rule=models.ForeignKey(to='project.FactoryRule', on_delete=models.CASCADE, related_name='project_factory_rule',null=True,blank=True,verbose_name="厂规")
    factory_rule_status = models.CharField(max_length=10, choices=(('no', '否'), ('yes', '是')), default='no',null=True,blank=True,verbose_name="厂规状态")
    customer_rule = models.ForeignKey(to='project.CustomerRule', on_delete=models.CASCADE,
                                     related_name='project_customer_rule', null=True, blank=True, verbose_name="客规")
    customer_rule_status = models.CharField(max_length=10, choices=(('no', '否'), ('yes', '是')), default='no',null=True,blank=True,verbose_name="客规状态")
    create_type = models.CharField(max_length=10, choices=(('create', '创建'), ('share', '分享')), default='create',
                                            verbose_name="工程来源")
    status = models.CharField(max_length=10, choices=(('draft', '草稿'), ('published', '已发布')), default='draft')

    objects = models.Manager()  # 默认的管理器
    published = ProjectManager()  # 自定义管理器
    tags=TaggableManager()

    class Meta:
        db_table = 'project'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('project:ProjectFormView', args=[self.id,])

    def __str__(self):
        # Return a string that represents the instance
        return self.name

class FactoryRule(models.Model):
    factory_rule_name=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="厂规名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True, related_name='project_factory_rule_user', verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')
    objects = models.Manager()  # 默认的管理器


    class Meta:
        db_table = 'project_factory_rule'
        ordering = ('-publish',)
    def get_absolute_url(self):
        return reverse('project:FactoryRuleFormView', args=[self.id,])
    def get_absolute_url_edit(self):
        return reverse('project:FactoryRuleUpdateView', args=[self.id,])

class CustomerRule(models.Model):
    customer_rule_name=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="客规名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True, related_name='project_customer_rule_user', verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')
    objects = models.Manager()  # 默认的管理器


    class Meta:
        db_table = 'project_customer_rule'
        ordering = ('-publish',)
    def get_absolute_url(self):
        return reverse('project:CustomerRuleFormView', args=[self.id,])
    def get_absolute_url_edit(self):
        return reverse('project:CustomerRuleUpdateView', args=[self.id,])


