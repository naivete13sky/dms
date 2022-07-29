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
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器MinLengthValidator
    # FileField 为文件上传功能upload_to:对应的files创建的文件夹目录
    file_odb = models.FileField(upload_to='files',blank=True, null=True,verbose_name="EP-ODB++")
    file_compressed = models.FileField(upload_to='files',blank=True, null=True,verbose_name="原始文件")
    file_org_type=models.CharField(max_length=10, choices=(('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'),
                                                           ('odb++', 'ODB++'), ('else', '其它')), default='else',verbose_name="原始料号类型")
    file_odb_current = models.FileField(upload_to='files', blank=True, null=True, verbose_name="最新-EP-ODB++")
    file_odb_g = models.FileField(upload_to='files', blank=True, null=True, verbose_name="G-ODB++")
    vs_result_ep=models.CharField(max_length=10, choices=(('success', '成功'), ('failed', '失败'), ('none', '未比对')), default='none',verbose_name="悦谱比图结果")
    vs_result_g = models.CharField(max_length=10, choices=(('success', '成功'), ('failed', '失败'), ('none', '未比对')),
                                    default='none',verbose_name="G软件比图结果")
    # drill_excellon2_units=models.CharField(max_length=10, choices=(('Inch', 'Inch'), ('MM', 'MM')), default='Inch',verbose_name="E2_units")
    # drill_excellon2_zeroes_omitted = models.CharField(max_length=10, choices=(('Leading', 'Leading'), ('Trailing', 'Trailing'), ('none', 'None')), default='Leading',verbose_name="E2省零")
    # drill_excellon2_number_format_A = models.CharField(max_length=10, choices=(('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')),
    #                                                    default='2',verbose_name="E2_format_A")
    # drill_excellon2_number_format_B = models.CharField(max_length=10, choices=(
    # ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')),
    #                                                    default='5', verbose_name="E2_format_B")
    # drill_excellon2_tool_units = models.CharField(max_length=10, choices=(('Inch', 'Inch'), ('MM', 'MM'), ('Mils', 'Mils')), default='Mils',
    #                                          verbose_name="E2_tool")
    job_name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="料号名称")
    job_type = models.CharField(max_length=10, choices=(('common', '普通板'), ('hdi', 'HDI'), ('led', 'LED板'), ('else', '其它')), default='common',
                                verbose_name="料号类型")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],verbose_name="备注",blank=True,null=True)

    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_jobs',null=True,blank=True,verbose_name="负责人")
    from_object=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)],null=True,blank=True,verbose_name="料号来源")
    publish = models.DateTimeField(default=timezone.now,null=True,blank=True,verbose_name='发布时间')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    STATUS_CHOICES = (('draft', '草稿'), ('published', '正式'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # 默认的管理器
    published = JobManager()  # 自定义管理器
    tags=TaggableManager()

    class Meta:
        db_table = 'job'
        ordering = ('-create_time',)
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


class Layer(models.Model):
    pass
    job = models.ForeignKey(to="job_manage.Job", on_delete=models.CASCADE,null=True,blank=True, related_name='job_manage_layer',verbose_name="料号名称")

    layer=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=1)],
                            verbose_name="层名称")
    layer_file_type=models.CharField(max_length=10, choices=(('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'), ('excellon2', 'Excellon2'),
                                                         ('excellon1', 'Excellon1'),('dxf', 'DXF'),
                                                             ('else', '其它')), default='else',verbose_name="层文件类型")

    layer_type = models.CharField(max_length=20, choices=(('signal_outter', '外层'),  ('signal_inner', '内层'),('solder', '防焊'),('silk', '丝印'),('paste', '锡膏'),
    ('drill', '孔层'), ('rout', 'Rout'), ('slot', '槽孔'), ('else', '其它')), default='else', verbose_name="层类型")
    features_count=models.IntegerField(default=0,null=True,blank=True,
                                     validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],verbose_name="物件数")


    drill_excellon2_units = models.CharField(max_length=10, choices=(('Inch', 'Inch'), ('MM', 'MM'), ('none', '未记录')), default='none',
                                             verbose_name="E2_units")
    drill_excellon2_zeroes_omitted = models.CharField(max_length=10, choices=(
    ('Leading', 'Leading'), ('Trailing', 'Trailing'), ('none', '未记录')), default='none', verbose_name="E2省零")
    drill_excellon2_number_format_A = models.CharField(max_length=10, choices=(
    ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')),
                                                       default='none', verbose_name="E2_format_A")
    drill_excellon2_number_format_B = models.CharField(max_length=10, choices=(
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')),
                                                       default='none', verbose_name="E2_format_B")
    drill_excellon2_tool_units = models.CharField(max_length=10,
                                                  choices=(('Inch', 'Inch'), ('MM', 'MM'), ('Mils', 'Mils'), ('none', '未记录')),
                                                  default='none',
                                                  verbose_name="E2_tool")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_layer_user', null=True, blank=True,
                               verbose_name="负责人")
    remark = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=1)],
                              verbose_name="备注", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        db_table = 'layer'
        ordering = ('-create_time',)
    # def get_absolute_url(self):
    #     return reverse('job_manage:JobFormView', args=[self.id, ])
    def __str__(self):
        # Return a string that represents the instance
        return self.layer