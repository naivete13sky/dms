from django.db import models
from django.core import validators
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Carriage(models.Model):
        name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                                verbose_name="车厢名称")
        remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                                  verbose_name="备注", blank=True)
        carriage_type = models.CharField(max_length=10, choices=(('head', '车头'), ('mid', '中间'), ('tail', '车尾')), default='head',null=True, blank=True,
                                          verbose_name="车厢类型")
        carriage_use=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                                verbose_name="车厢用途")
        check_set= models.CharField(max_length=10,choices=(('no', '无需审核'), ('yes', '需要审核')), default='no', null=True, blank=True, verbose_name="是否需要审核")


        author_exe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='process_carriage_author_exe_user',
                                   verbose_name="执行人")
        author_check = models.ForeignKey(User, on_delete=models.CASCADE, related_name='process_carriage_author_check_user',null=True,blank=True,
                                       verbose_name="审核人")
        author_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name='process_carriage_author_create_user',
                                       verbose_name="创建人")




        publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
        create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
        updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

        objects = models.Manager()  # 默认的管理器

        class Meta:
            db_table = 'process_carriage'
            ordering = ('-publish',)

        def get_absolute_url(self):
            return reverse('process:CarriageFormView', args=[self.id, ])
        def __str__(self):
            # Return a string that represents the instance
            return self.name

class Train(models.Model):
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                            verbose_name="火车名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                              verbose_name="备注", blank=True)
    train_use = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                                    verbose_name="火车用途")

    train_author_create = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name='process_train_author_create_user',
                                      verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = models.Manager()  # 默认的管理器

    class Meta:
        db_table = 'process_train'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('process:TrainFormView', args=[self.id, ])
    def __str__(self):
        # Return a string that represents the instance
        return self.name

class TrainSet(models.Model):
    pass
    name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                            verbose_name="名称")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],
                              verbose_name="备注", blank=True)
    order_id=models.IntegerField(blank=True,null=True,verbose_name="序号")
    train=models.ForeignKey(to='process.Train', on_delete=models.CASCADE, related_name='process_train_set_for_train',null=True,blank=True,verbose_name="归属火车")
    current_carriage=models.ForeignKey(to='process.Carriage', on_delete=models.CASCADE, related_name='process_train_set_current',null=True,blank=True,verbose_name="当前车厢")
    pre_carriage = models.ForeignKey(to='process.Carriage', on_delete=models.CASCADE,
                                         related_name='process_train_set_pre', null=True, blank=True,
                                         verbose_name="上一节车厢")
    post_carriage = models.ForeignKey(to='process.Carriage', on_delete=models.CASCADE,
                                         related_name='process_train_set_post', null=True, blank=True,
                                         verbose_name="下一节车厢")
    current_carriage_author_create = models.ForeignKey(User, on_delete=models.CASCADE,
                                            related_name='process_train_set_current_carriage_author_create',
                                            verbose_name="创建人")
    publish = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = models.Manager()  # 默认的管理器

    class Meta:
        db_table = 'process_train_set'
        # ordering = ('-publish',)
        ordering = ('order_id',)
    def get_absolute_url(self):
        return reverse('process:TrainSetFormView', args=[self.id, ])
    def __str__(self):
        # Return a string that represents the instance
        return self.name


