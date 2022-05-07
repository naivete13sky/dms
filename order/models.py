from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from djmoney.models.fields import MoneyField
from project.models import Project
from django.db.models import JSONField
# Create your models here.
class CamOrderManager(models.Manager):
    def get_queryset(self):
        return super(CamOrderManager, self).get_queryset().filter(status ='published')


class CamOrder(models.Model):
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],verbose_name="订单名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],verbose_name="备注",blank=True)
    customer_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cam_order_customer_user',verbose_name="下单人")
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cam_order_project',verbose_name="工程")
    customer_price=MoneyField(max_digits=14, decimal_places=2,null=True,blank=True, default_currency='Yuan',verbose_name='下单报价')
    should_finish_time=models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name="应交付时间")
    process_price=MoneyField(max_digits=14, decimal_places=2,null=True,blank=True, default_currency='Yuan',verbose_name='接单报价')
    process_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name='cam_order_process_user',verbose_name="接单人")
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='cam_order_author_user',verbose_name="负责人")
    status = models.CharField(
        max_length=10,
        choices=(('ToBeAccept', '未接单'), ('processing', '制作中'),('EQing', 'EQ中'),
                 ('ToBeCheck', '已提交待验收'),('passed', '验收通过'),('failed', '验收未通过')
                 ), default='ToBeAccept',null=True,blank=True,verbose_name="订单状态")
    process_times=models.IntegerField(null=True,blank=True,verbose_name="制作次数")

    publish = models.DateTimeField(default=timezone.now,verbose_name="发布时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    last_update_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cam_order_last_user',null=True,blank=True,verbose_name="最后一次更新人")
    cam_order_type = models.CharField(max_length=10, choices=(('create', '创建'), ('share', '分享')), default='create',
                                            verbose_name="订单类型")
    objects = models.Manager()  # 默认的管理器
    published = CamOrderManager()  # 自定义管理器
    tags=TaggableManager()

    class Meta:
        db_table = 'cam_order'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('order:CamOrderFormView', args=[self.id,])
    def __str__(self):
        return self.name




class CamOrderProcess(models.Model):
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                            verbose_name="订单流程名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True)
    cam_order=models.ForeignKey(to='order.CamOrder', on_delete=models.CASCADE,null=True,blank=True, related_name='cam_order_process', verbose_name="CAM代工服务订单")
    data = JSONField(db_index=True,null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cam_order_process_author_user', verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = models.Manager()  # 默认的管理器

    class Meta:
        db_table = 'cam_order_process'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('order:CamOrderProcessFormView', args=[self.id, ])
    def __str__(self):
        return self.name
