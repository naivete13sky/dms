from django.db import models
from django.conf import settings
from django.core import validators  # 自定义验证器
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


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

