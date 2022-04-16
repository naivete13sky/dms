from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Org(models.Model):
    file_org = models.FileField(upload_to='router_job_org', verbose_name="原始料号")
    RECIPE_STATUS_CHOICES = (('yes', 'yes'), ('no', 'no'))
    company_name = models.CharField(max_length=250, verbose_name="公司名称")
    job_name_org = models.CharField(max_length=250,verbose_name="原始料号名称")
    slug = models.SlugField(max_length=250, unique_for_date='receive_date')
    receive_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='use_org',verbose_name="料号负责人")
    receive_date = models.DateTimeField(default=timezone.now,verbose_name="接受料号时间")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipe_status = models.CharField(max_length=10, choices=RECIPE_STATUS_CHOICES, default='no',verbose_name="是否提供了参数")
    remark = models.TextField(verbose_name="备注")

    class Meta:
        ordering = ('-receive_date',)
        verbose_name = '原始料号'
        verbose_name_plural = '原始料号'

    def __str__(self):
        return self.job_name_org



    def file_link(self):
        if self.file_org:
            return "<a href='%s'>download</a>" % (self.file_org.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True


class Pre(models.Model):
    job_name_org = models.ForeignKey(Org, related_name='org_pre', on_delete=models.CASCADE, verbose_name="原始料号名称")
    file_pre = models.FileField(upload_to='router_job_pre', verbose_name="前处理料号")
    PRE_STATUS_CHOICES = (('yes', 'yes'), ('no', 'no'))
    job_name_pre = models.CharField(max_length=250,verbose_name="前处理料号名称")
    slug = models.SlugField(max_length=250, unique_for_date='pre_date')
    pre_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_pre',verbose_name="前处理料号负责人")
    pre_date = models.DateTimeField(default=timezone.now,verbose_name="前处理料号时间")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pre_status = models.CharField(max_length=10, choices=PRE_STATUS_CHOICES, default='no',verbose_name="是否完成了前处理")
    remark = models.TextField(verbose_name="备注")



    class Meta:
        ordering = ('-pre_date',)
        verbose_name = '前处理料号'
        verbose_name_plural = '前处理料号'

    def __str__(self):
        return self.job_name_pre



class Job_view(models.Model):
    pass
    class Meta:

        verbose_name = '料号情况查询'
        verbose_name_plural = '料号情况查询'