from django.db import models
from django.conf import settings
from django.core import validators  # 自定义验证器

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    mobile=models.CharField(blank=True,max_length=13, validators=[validators.MinLengthValidator(limit_value=13)],verbose_name="手机号")
    recommender=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True,related_name='account_recommender')
    cam_level=models.CharField(max_length=10,
                               choices=(('level1', '等级1'),
                                        ('level2', '等级2'),
                                        ('level3', '等级3'),
                                        ('level4', '等级4'),
                                        ('level5', '等级5')),
                               # default='level1',
                               blank=True,null=True)


    def __str__(self):
        return "Profile for user {}".format(self.user.username)