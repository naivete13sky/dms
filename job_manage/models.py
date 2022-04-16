from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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