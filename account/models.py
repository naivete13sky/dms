import os

from django.db import models
from django.conf import settings
from django.core import validators  # 自定义验证器
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import json
from django.conf import settings



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    mobile=models.CharField(blank=True,max_length=11, validators=[validators.MinLengthValidator(limit_value=11)],verbose_name="手机号")
    # recommender=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True,related_name='account_recommender')
    recommender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name='account_recommender')
    cam_level=models.CharField(max_length=10,
                               choices=(('level1', '等级1'),
                                        ('level2', '等级2'),
                                        ('level3', '等级3'),
                                        ('level4', '等级4'),
                                        ('level5', '等级5')),
                               # default='level1',
                               blank=True,null=True)
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)

class FactoryRule(models.Model):
    pass
    factory_rule_name=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="厂规名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True,null=True)
    # slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True, related_name='account_factory_rule_user', verbose_name="创建人")
    # author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True,
    #                            related_name='account_factory_rule_profile', verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # 默认的管理器


    class Meta:
        db_table = 'factory_rule'
        ordering = ('-publish',)
    def get_absolute_url(self):
        return reverse('factoryruleformview', args=[self.id,])
    def get_absolute_url_edit(self):
        return reverse('factoryrule_update', args=[self.id,])

class CustomerRule(models.Model):
    customer_rule_name=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="客规名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True, related_name='account_customer_rule_user', verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # 默认的管理器


    class Meta:
        db_table = 'customer_rule'
        ordering = ('-publish',)
    def get_absolute_url(self):
        return reverse('CustomerRuleFormView', args=[self.id,])
    def get_absolute_url_edit(self):
        return reverse('CustomerRuleUpdateView', args=[self.id,])

class QueryData(models.Model):

    query_job_file_usage_type=models.CharField(max_length=20,blank=True,null=True,
                                               choices=(('all','所有'), ('input_test','导入测试'), ('customer_job','客户资料'), ('test','测试'), ('else','其它')),
                                               default='all',help_text='此用户筛选条件记录用的',verbose_name='筛选-料号使用类型')

    query_job_job_name = models.CharField(blank=True,null=True,max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],
                              help_text='此用户筛选条件记录用的',verbose_name="筛选-料号名", )
    query_job_author = models.CharField(blank=True, null=True, max_length=100,
                                          validators=[validators.MinLengthValidator(limit_value=0)],
                                          help_text='此用户筛选条件记录用的', verbose_name="筛选-负责人", )
    query_job_from_object = models.CharField(blank=True, null=True, max_length=100,
                                          validators=[validators.MinLengthValidator(limit_value=0)],
                                          help_text='此用户筛选条件记录用的', verbose_name="筛选-料号来源", )

    query_job_paginator_page = models.IntegerField(default=10,null=True,blank=True,
                                     validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(5)],help_text="每页显示行数",verbose_name='query_job_paginator_page')

    query_job_file_odb_current = models.CharField(max_length=20, blank=True, null=True,
                                                 choices=(
                                                 ('all', '所有'), ('no', '无'), ('yes', '有'),),
                                                 default='all', help_text='此用户筛选条件记录用的', verbose_name='筛选-是否存在悦谱最新转图')

    query_job_status = models.CharField(max_length=20, blank=True, null=True,
                                                  choices=(
                                                      ('all', '所有'), ('draft', '草稿'), ('published', '正式'),),
                                                  default='all', help_text='此用户筛选条件记录用的', verbose_name='筛选-状态')

    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                              verbose_name="备注", blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True, related_name='account_query_data_user', verbose_name="用户")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')
    objects = models.Manager()  # 默认的管理器


    class Meta:
        db_table = 'account_query_data'
        ordering = ('-publish',)

class Customer(models.Model):
    name_full = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],null=True,blank=True,verbose_name="客户全称")
    name_simple = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],null=True,blank=True,verbose_name="客户简称")
    department = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],null=True,blank=True,verbose_name="部门")


    # name = models.CharField('标题', max_length=256,null=True,blank=True)
    country = models.CharField('国家', max_length=256,null=True,blank=True)
    province = models.CharField('省份', max_length=256,null=True,blank=True)
    city = models.CharField('城市', max_length=256,null=True,blank=True)



    customer_type=models.CharField(max_length=20, choices=(('pcb_factory', '板厂'), ('design_customer', '设计端客户')), default='pcb_factory',
                                   null=True,blank=True,verbose_name="客户类型")

    remark = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)], blank=True,
                              null=True, help_text='备注', verbose_name="备注")
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        # return "Profile for customer {}".format(self.name_simple)
        return self.name_simple

    def get_absolute_url(self):
        return reverse('CustomerDetailView', args=[self.id, ])