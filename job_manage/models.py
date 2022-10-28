# Create your models here.
from functools import reduce

from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core import validators  # 自定义验证器
from django.urls import reverse
from taggit.managers import TaggableManager
from taggit.models import TagBase,GenericTaggedItemBase
from django.utils.text import slugify
from django.utils.translation import gettext, gettext_lazy as _
from account.models import Customer

class MyTag(TagBase):
    # 这一步是关键，要设置allow_unicode=True，这样这个字段才能支持中文
    slug = models.SlugField(verbose_name=_("slug"), unique=True, max_length=100, allow_unicode=True)

    # 这个方法也是要覆盖的，它是用来计算slug的，也是添加allow_unicode=True参数
    def slugify(self, tag, i=None):
        slug = slugify(tag, allow_unicode=True)
        if i is not None:
            slug += "_%d" % i
        return slug

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        app_label = "taggit"


class TaggedWhatever(GenericTaggedItemBase):
    # 把我们自定义的模型类传进来，它就能知道如何处理
    tag = models.ForeignKey(
        MyTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class JobManager(models.Manager):
    def get_queryset(self):
        return super(JobManager, self).get_queryset().filter(status ='published')
        # return super(JobManager, self).get_queryset().all()

class Job(models.Model):
    # ------------------------------------------------基础字段，主要为了导入测试用的-------------------------------------------
    file_usage_type = models.CharField(max_length=50,
                                       choices=(('input_test', '导入测试'), ('customer_job', '客户资料'),
                                                ('test', '测试'), ('else', '其它')), default='else', help_text='料号使用类型',
                                       verbose_name="料号使用类型")
    # 当我们想设置最小长度的时候，但是在字段中没有的话，可以借助自定义验证器MinLengthValidator
    # FileField 为文件上传功能upload_to:对应的files创建的文件夹目录
    file_compressed = models.FileField(upload_to='files', blank=True, null=True,
                                       help_text='整理过的原始文件.若是导入测试类型,则是rar压缩包,压缩包中只有一层文件夹.也可以是.tgz|.eps', verbose_name="整理过的原始文件")
    job_name = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=3)],
                                help_text='料号名称,有可能有重复名字', verbose_name="料号名称")
    file_odb_g = models.FileField(upload_to='files', blank=True, null=True, help_text='G软件转图的结果,导入测试类型需要填写此字段',
                                  verbose_name="G-ODB++")
    file_compressed_org = models.FileField(upload_to='files', blank=True, null=True, help_text='未整理的原始文件,rar压缩包',verbose_name="原始文件")
    file_org_type = models.CharField(max_length=10,
                                     choices=(('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'),
                                              ('odb++', 'ODB++'), ('eps', 'EPS'),('else', '其它')), default='else',
                                     help_text='原始文件类型', verbose_name="原始文件类型")
    from_object = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=2)], null=True,
                                   blank=True, help_text='料号从哪来的', verbose_name="料号来源")
    from_object_pcb_factory = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='job_manage_job_account_customer_pcb_factory', null=True, blank=True,
                               help_text='料号来源-板厂', verbose_name="料号来源-板厂")
    from_object_pcb_design = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                        related_name='job_manage_job_account_customer_pcb_design', null=True, blank=True,
                                        help_text='料号来源-设计端', verbose_name="料号来源-设计端")
    status = models.CharField(max_length=10, choices=(('draft', '草稿'), ('published', '正式')), default='draft',
                              help_text='草稿表示未经人工确认', )
    # tags=TaggableManager()
    # 声明这个manager也是基于我们自定义的模型类
    tags = TaggableManager(through=TaggedWhatever,help_text='必填')
    remark = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)], blank=True,
                              null=True, help_text='料号的说明备注', verbose_name="备注")

    file_odb_current = models.FileField(upload_to='files', blank=True, null=True, help_text='最新一次的悦谱转图结果,不需要手工录入,可在线自动生成',verbose_name="最新-EP-ODB++")
    vs_result_ep=models.CharField(max_length=10, choices=(('passed', '成功'), ('failed', '失败'), ('none', '未比对')), default='none',help_text='导入测试管理员负责填写',verbose_name="悦谱比图结果")
    vs_result_g = models.CharField(max_length=10, choices=(('passed', '成功'), ('failed', '失败'), ('none', '未比对')),
                                    default='none',help_text='导入测试管理员负责填写',verbose_name="G软件比图结果")
    bug_info = models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=0)],blank=True, null=True,help_text='Bug信息',verbose_name="Bug信息")
    bool_layer_info = models.CharField(max_length=10, choices=(('true', 'true'), ('false', 'false')), default='false',
                                       null=True, blank=True, help_text='不需要人工填写,系统用', verbose_name="是否有层别信息")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_jobs', null=True, blank=True,
                               help_text='料号上传人', verbose_name="负责人")
    publish = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='发布时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    vs_time_ep = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                                  null=True, blank=True, help_text='系统生成', verbose_name="悦谱比对时间戳")
    vs_time_g = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                                 null=True, blank=True, help_text='系统生成', verbose_name="G比对时间戳")

    objects = models.Manager()  # 默认的管理器
    published = JobManager()  # 自定义管理器





    # ------------------------------------------------整理好的料号信息-------------------------------------------
    file_odb = models.FileField(upload_to='files', blank=True, null=True, help_text='整理好的ODB++资料,确认过是对的',
                                verbose_name="整理好的ODB++资料")

    hasOrig = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                                  help_text="是否有orig?", verbose_name="是否有orig")
    hasNet = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                               help_text="是否有net?", verbose_name="是否有net")
    hasPre = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                               help_text="是否有pre?", verbose_name="是否有pre")
    hasPcs = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                               help_text="是否有pcs?", verbose_name="是否有pcs")
    hasSet = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                               help_text="是否有set?", verbose_name="是否有set")
    hasPanel = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                               help_text="是否有panel?", verbose_name="是否有panel")





    #------------------------------------------------所有层相关的-------------------------------------------
    job_type = models.CharField(max_length=10, choices=(('common', '普通板'), ('hdi', 'HDI'), ('led', 'LED板'), ('car', '汽车板'), ('flex', '软板'),
                                                         ('rigid_flex', '软硬结合板'),('carrier', '载板'), ('else', '其它')), default='common',
                                help_text='料号的类型',verbose_name="料号类型")
    job_type_1 = models.CharField(max_length=20, choices=(('through_hole', '通孔板'), ('non_through_hole', '非通孔板'), ('else', '其它')), default='else',
                                blank=True,null=True,help_text='料号的类型-维度1', verbose_name="料号类型-维度1")
    job_type_2 = models.CharField(max_length=20,
                                  choices=(('rigid', '硬板'), ('flex', '软板'),('rigid_flex', '软硬结合板'), ('else', '其它')),
                                  default='else',
                                  blank=True, null=True, help_text='料号的类型-维度2', verbose_name="料号类型-维度2")
    job_type_3 = models.CharField(max_length=20,
                                  choices=(('ic', 'IC载板'), ('led', 'LED灯板'), ('car', '汽车板'), ('server', '服务器板'), ('else', '其它')),
                                  default='else',
                                  blank=True, null=True, help_text='料号的类型-维度3', verbose_name="料号类型-维度3")
    pcsSize = models.FloatField(null=True, blank=True, help_text='pcs的profile线外接正矩形的对角线长度(单位:inch)',
                                verbose_name='pcs对角线尺寸')
    matrixRowNum = models.IntegerField(null=True, blank=True,
                                       validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(0)],
                                       help_text="所有层数(包括任意层)", verbose_name='所有层数')
    totalFeatureNum = models.IntegerField(null=True, blank=True,
                                          validators=[validators.MaxValueValidator(100000000),
                                                      validators.MinValueValidator(0)], help_text="总物件数",
                                          verbose_name='总物件数')

    # ------------------------------------------------线路层相关的-------------------------------------------
    copperLayerNum = models.IntegerField(null=True, blank=True,validators=[validators.MaxValueValidator(1000),validators.MinValueValidator(0)],
                                         help_text="信号层数量(含地电层)",verbose_name='信号层数')
    pgLayerNum = models.IntegerField(null=True, blank=True, validators=[validators.MaxValueValidator(1000),
                                                                            validators.MinValueValidator(0)],
                                         help_text="地电层数量", verbose_name='地电层数')
    hasPGlayer = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                                  help_text="是否有地电层(负片层)", verbose_name="是否有地电层(负片层)")
    linedCopper = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                                   help_text="线路层是否为线铜", verbose_name="线路层是否为线铜")

    bgaNumTop = models.IntegerField(null=True, blank=True,
                                 validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],
                                 help_text="正面BGA总数", verbose_name='正面BGA总数')

    bgaNumBottom = models.IntegerField(null=True, blank=True,
                                 validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],
                                 help_text="背面BGA总数", verbose_name='背面BGA总数')


    bgaNum = models.IntegerField(null=True, blank=True,
                                 validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],
                                 help_text="BGA总数", verbose_name='BGA总数')
    impLineNum = models.IntegerField(null=True, blank=True,
                                     validators=[validators.MaxValueValidator(100000), validators.MinValueValidator(0)],
                                     help_text="阻抗线数", verbose_name='阻抗线数')

    minLineWidth4outerTop = models.FloatField(null=True, blank=True, help_text='正面外层的最小线宽(单位:mil)', verbose_name='正面外层最小线宽')
    minLineSpace4outerTop = models.FloatField(null=True, blank=True, help_text='正面外层的最小线距(单位:mil)', verbose_name='正面外层最小线距')

    minLineWidth4outerBottom = models.FloatField(null=True, blank=True, help_text='背面外层的最小线宽(单位:mil)', verbose_name='背面外层最小线宽')
    minLineSpace4outerBottom = models.FloatField(null=True, blank=True, help_text='背面外层的最小线距(单位:mil)', verbose_name='背面外层最小线距')


    minLineWidth4outer = models.FloatField(null=True, blank=True, help_text='外层的最小线宽(单位:mil)', verbose_name='外层最小线宽')
    minLineSpace4outer = models.FloatField(null=True, blank=True, help_text='外层的最小线距(单位:mil)', verbose_name='外层最小线距')

    # ------------------------------------------------防焊层相关的-------------------------------------------
    solderWindowNumTop = models.IntegerField(null=True, blank=True,
                                                        validators=[validators.MaxValueValidator(100000000),
                                                                    validators.MinValueValidator(0)],
                                                        help_text="正面防焊层物件数,如果有多层，填写总数）", verbose_name='正面防焊层物件数（总数）')
    solderWindowNumBottom = models.IntegerField(null=True, blank=True,
                                             validators=[validators.MaxValueValidator(100000000),
                                                         validators.MinValueValidator(0)],
                                             help_text="底面防焊层物件数,如果有多层，填写总数）", verbose_name='底面防焊层物件数（总数）')
    solderMaxWindowNum4singleSide = models.IntegerField(null=True, blank=True,
                                                        validators=[validators.MaxValueValidator(100000000),
                                                                    validators.MinValueValidator(0)],
                                                        help_text="单面最多防焊开窗数量", verbose_name='单面最多防焊开窗数量')
    hasSMlayer = models.CharField(max_length=10, choices=(('yes', '是'), ('no', '否'), ('none', 'None')), default='none',
                                  help_text="是否有防焊层?", verbose_name="是否有防焊层")

    # ------------------------------------------------孔层相关的-------------------------------------------
    pcsDrlNum = models.IntegerField(null=True, blank=True,
                                    validators=[validators.MaxValueValidator(100000000),
                                                validators.MinValueValidator(0)], help_text="所有孔层的所有孔数量(包括槽孔,镭射孔等)",
                                    verbose_name='pcs所有孔数')

    hdiLevel = models.IntegerField(null=True, blank=True,
                                   validators=[validators.MaxValueValidator(99), validators.MinValueValidator(0)],
                                   help_text="孔阶数，HDI介数", verbose_name='孔阶数')








    # ------------------------------------------------梅需要的其它字段-------------------------------------------
    usage=models.CharField(null=True,blank=True,max_length=200, validators=[validators.MinLengthValidator(limit_value=0)],help_text="料号用途",verbose_name='用途')
    job_url=models.URLField(null=True,blank=True,verbose_name="料号url")
    origStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="原稿step名称",verbose_name='orig_step')
    prepareStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="前处理完成的step名称",verbose_name='pre_step')
    pcsStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="已经完成pcs处理的step名",verbose_name='pcs_step')
    setStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="set拼板完成的step名",verbose_name='set_step')
    panelStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="panel拼板完成的step名",verbose_name='panel_step')
    impCouponStepName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="阻抗测试条的step名",verbose_name='阻抗step')
    routLayerName=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="rout层的名字",verbose_name='Rout层')
    panelSize=models.FloatField(null=True,blank=True,help_text='panel的profile线外接正矩形的对角线长度(单位:inch)',verbose_name='panel对角线尺寸')
    customerCode=models.CharField(null=True,blank=True,max_length=50, validators=[validators.MinLengthValidator(limit_value=0)],help_text="客户(代码)",verbose_name='客户(代码)')




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

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

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

    layer=models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],
                            verbose_name="层名称")
    layer_org=models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],null=True,blank=True,
                            verbose_name="原始层名称")
    vs_result_manual = models.CharField(max_length=10, choices=(('passed', '通过'), ('failed', '失败'), ('none', '未比对')),
                                    default='none', null=True, blank=True, verbose_name="人工比对结果")
    vs_result_ep = models.CharField(max_length=10, choices=(('passed', '通过'), ('failed', '失败'), ('none', '未比对')),
                                 default='none', null=True, blank=True, verbose_name="悦谱比对结果")
    vs_result_g = models.CharField(max_length=10, choices=(('passed', '通过'), ('failed', '失败'), ('none', '未比对')),
                                    default='none', null=True, blank=True, verbose_name="G软件比对结果")

    layer_file_type=models.CharField(max_length=100, choices=(('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'), ('excellon2', 'Excellon2'),
                                                         ('excellon1', 'Excellon1'),('dxf', 'DXF'),
                                                             ('else', '其它')), default='else',verbose_name="层文件类型")

    layer_type = models.CharField(max_length=100, choices=(('signal_outter', '外层'),  ('signal_inner', '内层'),('solder', '防焊'),('silk', '丝印'),('paste', '锡膏'),
    ('drill', '孔层'), ('rout', 'Rout'), ('slot', '槽孔'), ('else', '其它')), default='else', verbose_name="层类型")
    features_count=models.IntegerField(default=0,null=True,blank=True,
                                     validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],verbose_name="物件数")


    units_ep = models.CharField(max_length=10, choices=(('Inch', 'Inch'), ('MM', 'MM'), ('none', '未记录')), default='none',
                                             verbose_name="units_EP")

    coordinates_ep = models.CharField(max_length=20, choices=(('Absolute', 'Absolute'), ('Incremental', 'Incremental'), ('none', '未记录')),
                                default='none',
                                verbose_name="coordinates_ep")

    zeroes_omitted_ep = models.CharField(max_length=10, choices=(
    ('Leading', 'Leading'), ('Trailing', 'Trailing'), ('none', '未记录')), default='none', verbose_name="省零EP")
    number_format_A_ep = models.CharField(max_length=10, choices=(
    ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')),
                                                       default='none', verbose_name="整数EP")
    number_format_B_ep = models.CharField(max_length=10, choices=(
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('none', '未记录')),
                                                       default='none', verbose_name="小数EP")
    tool_units_ep = models.CharField(max_length=10,
                                                  choices=(('Inch', 'Inch'), ('MM', 'MM'), ('Mils', 'Mils'), ('none', '未记录')),
                                                  default='none',
                                                  verbose_name="Tool_units_EP")

    units_g = models.CharField(max_length=10, choices=(('Inch', 'Inch'), ('MM', 'MM'), ('none', '未记录')),
                                default='none',verbose_name="units_G")
    coordinates_g = models.CharField(max_length=20, choices=(
    ('Absolute', 'Absolute'), ('Incremental', 'Incremental'), ('none', '未记录')),
                                      default='none',
                                      verbose_name="coordinates_g")
    zeroes_omitted_g = models.CharField(max_length=10, choices=(
        ('Leading', 'Leading'), ('Trailing', 'Trailing'), ('none', '未记录')), default='none', verbose_name="省零G")
    number_format_A_g = models.CharField(max_length=10, choices=(
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('none', '未记录')),default='none', verbose_name="整数G")
    number_format_B_g = models.CharField(max_length=10, choices=(
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('none', '未记录')), default='none', verbose_name="小数G")
    tool_units_g = models.CharField(max_length=10,
                                     choices=(('Inch', 'Inch'), ('MM', 'MM'), ('Mils', 'Mils'), ('none', '未记录')),
                                     default='none',
                                     verbose_name="Tool_units_G")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_layer_user', null=True, blank=True,
                               verbose_name="负责人")
    STATUS_CHOICES = (('draft', '草稿'), ('published', '正式'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    vs_time_ep = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                               null=True, blank=True, verbose_name="悦谱比对时间戳")
    vs_time_g = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                                  null=True, blank=True, verbose_name="G比对时间戳")
    remark = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],
                              verbose_name="备注", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    cc_test1=models.CharField(max_length=20, validators=[validators.MinLengthValidator(limit_value=0)],
                              verbose_name="cc_test", blank=True, null=True)

    class Meta:
        db_table = 'layer'
        ordering = ('-create_time',)


    def get_absolute_url(self):
        return reverse('job_manage:LayerFormView', args=[self.id, ])

    def __str__(self):
        # Return a string that represents the instance
        return self.layer

class Vs(models.Model):
    pass
    job = models.ForeignKey(to="job_manage.Job", on_delete=models.CASCADE,null=True,blank=True, related_name='job_manage_vs',verbose_name="料号名称")

    layer=models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],
                            verbose_name="层名称")
    layer_org=models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],null=True,blank=True,
                            verbose_name="原始层名称")
    vs_result=models.CharField(max_length=10, choices=(('passed', '通过'), ('failed', '失败'), ('none', '未比对')), default='none',null=True,blank=True,verbose_name="比对结果")
    vs_result_detail=models.CharField(max_length=1000000, validators=[validators.MinLengthValidator(limit_value=0)],
                            null=True,blank=True,verbose_name="比对详细信息")

    vs_method = models.CharField(max_length=10, choices=(('ep', '悦谱'), ('g', 'G软件'), ('none', 'none')),
                                    default='none', null=True, blank=True, verbose_name="比对方法")
    layer_file_type=models.CharField(max_length=100, choices=(('gerber274X', 'Gerber274-X'), ('gerber274D', 'Gerber274-D'), ('excellon2', 'Excellon2'),
                                                         ('excellon1', 'Excellon1'),('dxf', 'DXF'),
                                                             ('else', '其它')), default='else',verbose_name="层文件类型")

    layer_type = models.CharField(max_length=100, choices=(('signal_outter', '外层'),  ('signal_inner', '内层'),('solder', '防焊'),('silk', '丝印'),('paste', '锡膏'),
    ('drill', '孔层'), ('rout', 'Rout'), ('slot', '槽孔'), ('else', '其它')), default='else', verbose_name="层类型")
    features_count=models.IntegerField(default=0,null=True,blank=True,
                                     validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)],verbose_name="物件数")



    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_vs_user', null=True, blank=True,
                               verbose_name="负责人")
    STATUS_CHOICES = (('draft', '草稿'), ('published', '正式'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    vs_time_ep=models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                            null=True, blank=True,verbose_name="悦谱比对时间戳")
    vs_time_g = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                                  null=True, blank=True, verbose_name="G比对时间戳")

    remark = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],
                              verbose_name="备注", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        db_table = 'vs'
        ordering = ('-create_time',)
    # def get_absolute_url(self):
    #     return reverse('job_manage:JobFormView', args=[self.id, ])
    def __str__(self):
        # Return a string that represents the instance
        return self.layer


class Bug(models.Model):
    pass
    job = models.ForeignKey(to="job_manage.Job", on_delete=models.CASCADE,null=True,blank=True, related_name='job_manage_bug',verbose_name="料号名称")
    bug=models.CharField(max_length=200, validators=[validators.MinLengthValidator(limit_value=1)],null=True,blank=True,
                            verbose_name="Bug名称")
    bug_zentao_id=models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=1)],
                            verbose_name="禅道ID")
    bug_zentao_pri = models.CharField(max_length=10, choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('none', 'none')),
                                    default='none', null=True, blank=True, verbose_name="优先级")
    bug_zentao_status = models.CharField(max_length=10, choices=(('active', '激活'), ('closed', '已关闭'), ('resloved', '已解决'), ('none', 'none')),
                                      default='none', null=True, blank=True, verbose_name="禅道状态")
    bug_creator = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],null=True,blank=True,
                           verbose_name="创建者")
    bug_create_date = models.DateTimeField(null=True,blank=True,verbose_name='禅道创建时间')
    bug_assigned_to = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=1)],null=True,blank=True,
                                   verbose_name="指派给")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_manage_bug_user', null=True, blank=True,
                               verbose_name="负责人")
    status = models.CharField(max_length=10, choices=(('draft', '草稿'), ('published', '正式')), default='draft',null=True,blank=True,verbose_name="发布状态")
    refresh_time = models.CharField(max_length=10, validators=[validators.MinLengthValidator(limit_value=0)],
                               null=True, blank=True, verbose_name="刷新时间戳")
    remark = models.CharField(max_length=100, validators=[validators.MinLengthValidator(limit_value=0)],
                              verbose_name="备注", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        db_table = 'bug'
        ordering = ('-create_time',)

    def get_absolute_url(self):
        return reverse('job_manage:BugFormView', args=[self.id, ])

    def __str__(self):
        # Return a string that represents the instance
        return self.bug_zentao_id



