from django import forms
from django.forms import widgets
from job_manage import models
from django.forms import ModelForm
from django.forms.widgets import Textarea
from django import forms
from .models import Job,ShareAccount,Layer,Bug
from .models import Register
# forms.Form:代表着为导入表单
# forms.ModelForm:代表着导入模型的表单


class UserForm(forms.Form):
    username = forms.CharField(min_length=4, label='用户名',
                               widget=widgets.TextInput(attrs={"class": "form-control"}),
                               error_messages={
                                   "required": "用户名不能为空",
                               })
    pwd = forms.CharField(min_length=4, label='密码',
                          error_messages={
                              "required": "密码不能为空",
                          },
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    r_pwd = forms.CharField(min_length=4, label='确认密码',
                            widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                            error_messages={
                                "required": "密码不能为空",
                            })
    email = forms.EmailField(label='邮箱',
                             widget=widgets.EmailInput(attrs={"class": "form-control"}),
                             error_messages={
                                 "required": '邮箱不能为空',
                                 "invalid": "邮箱格式错误",
                             })
    tel = forms.CharField(label='手机号',
                          widget=widgets.TextInput(attrs={"class": "form-control"}),
                          )

class UploadForms(forms.ModelForm):
    """
    Meta : 该类是必须继承的,但是该字段是
    model :对应的模型类
    fields : 当为‘__all__就是验证全部字段’,当只想验证其中部分的字段的时候，需要使用[]包裹起来
    """
    class Meta:
        model = Job
        fields = '__all__'
        # 当只想验证某几个字段的情况下可以使用[]的形式
        # fields = ['title']  # 表示只验证title这个字段
        exclude = ['title']   # exclude->排除的意思  表示不验证title这个字段

        error_messages = {
            'job_name': {
                'required': '该字段是必须要填的',
                'min_length': '最小长度为3',
                'max_length': '最大长度为20'
            },
            'remark': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为100'
            },
            'author': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为15'
            }
        }

class UploadForms_no_file(forms.ModelForm):
    """
    Meta : 该类是必须继承的,但是该字段是
    model :对应的模型类
    fields : 当为‘__all__就是验证全部字段’,当只想验证其中部分的字段的时候，需要使用[]包裹起来
    """
    class Meta:
        model = Job
        fields = ['job_name','remark','author','publish','status']
        # 当只想验证某几个字段的情况下可以使用[]的形式
        # fields = ['title']  # 表示只验证title这个字段
        exclude = ['title']   # exclude->排除的意思  表示不验证title这个字段

        error_messages = {
            'job_name': {
                'required': '该字段是必须要填的',
                'min_length': '最小长度为3',
                'max_length': '最大长度为20'
            },
            'remark': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为100'
            },
            'author': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为15'
            }
        }

class AddForms(forms.ModelForm):
    """
    Meta : 该类是必须继承的,但是该字段是
    model :对应的模型类
    fields : 当为‘__all__就是验证全部字段’,当只想验证其中部分的字段的时候，需要使用[]包裹起来
    """
    class Meta:
        model = Job
        # fields = '__all__'
        # 当只想验证某几个字段的情况下可以使用[]的形式
        # fields = ['title']  # 表示只验证title这个字段
        exclude = ['title']   # exclude->排除的意思  表示不验证title这个字段

        error_messages = {
            'title': {
                'required': '该字段是必须要填的',
                'min_length': '最小长度为3',
                'max_length': '最大长度为20'
            },
            'content': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为100'
            },
            'author': {
                'required': '该字段是必须要填的',
                'max_length': '最大长度为15'
            }
        }

class RegisterForm(forms.ModelForm):
    pwd1 = forms.CharField(min_length=3, max_length=30)
    pwd2 = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(max_length=30)

    # clean映射多字段
    def clean(self):
        changed_data = super().clean()
        # print(changed_data)  # 该返回的是一个字典形式
        # changed_data:该返回是有变化的列表
        pwd1 = changed_data.get('pwd1')
        pwd2 = changed_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError('请输入两次相同的密码')

    class Meta:
        # 使用的模型
        model = Register
        # 不验证密码
        exclude = ['password']
        error_messages = {
            'telephone': {
                'required': '请填写该字段',
            },
            'email': {
                'required': '请填写该字段',
                'invalid': '请输入正确的邮箱地址'
            }
        }

class ViewForms(forms.ModelForm):
    pass

class JobFormsReadOnly(forms.ModelForm):
    """
    Meta : 该类是必须继承的,但是该字段是
    model :对应的模型类
    fields : 当为‘__all__就是验证全部字段’,当只想验证其中部分的字段的时候，需要使用[]包裹起来
    """
    class Meta:
        model = Job
        # fields = ['job_name','remark','slug','author','publish','status']
        # fields = ['job_name',]
        fields = '__all__'


        def __init__(self, *args, **kwargs):
            super(JobFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class ShareForm(forms.ModelForm):
    class Meta:
        model = ShareAccount
        fields = ['share_account','publish','remark']

class JobForm(forms.ModelForm):
    pass
    class Meta:
        model=Job
        fields = '__all__'
        fields = ['file_odb']

class JobForm2(forms.ModelForm):
    pass
    class Meta:
        model=Job
        fields = '__all__'


class JobFormCam(forms.ModelForm):
    # hasOrig = forms.CharField(disabled=True)
    class Meta:
        model=Job
        # fields = '__all__'
        fields = ['file_odb','hasOrig','hasNet','hasPre','hasPcs','hasSet','hasPanel',
                  'job_type_1','job_type_2','job_type_3','pcsSize','matrixRowNum','totalFeatureNum',
                  'copperLayerNum','pgLayerNum','hasPGlayer','linedCopper','bgaNumTop','bgaNumBottom','impLineNum',
                  'minLineWidth4outerTop','minLineSpace4outerTop','minLineWidth4outerBottom','minLineSpace4outerBottom',
                  'solderWindowNumTop','solderWindowNumBottom','hasSMlayer',
                  'pcsDrlNum','hdiLevel',
                  ]

        #让某些字段不可修改
        # def __init__(self, *args, **kwargs):
        #     super(JobFormCam, self).__init__(*args, **kwargs)
        #     for name, field in ['job_name']:
        #         field.widget.attrs['readonly'] = 'true'

#下面这个没用啦！
class JobFormCam_old_1(forms.ModelForm):
    pass
    class Meta:
        model=Job
        # fields = '__all__'
        fields = ['file_odb','hasOrig','hasNet','hasPre','hasPcs','hasSet','hasPanel',
                  'job_type_1','job_type_2','job_type_3','pcsSize','matrixRowNum','totalFeatureNum',
                  'copperLayerNum','pgLayerNum','hasPGlayer','linedCopper','bgaNum','impLineNum','minLineWidth4outer','minLineSpace4outer',
                  'solderWindowNumTop','solderWindowNumBottom','hasSMlayer',
                  'pcsDrlNum','hdiLevel',
                  ]

        #让某些字段不可修改
        # def __init__(self, *args, **kwargs):
        #     super(JobFormCam, self).__init__(*args, **kwargs)
        #     for name, field in ['job_name']:
        #         field.widget.attrs['readonly'] = 'true'

class LayerForm(forms.ModelForm):
    pass
    class Meta:
        model=Layer
        fields = '__all__'
        # fields = ['file_odb']


class LayerFormsReadOnly(forms.ModelForm):
    class Meta:
        model = Layer
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super(LayerFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'

class BugForm(forms.ModelForm):
    pass
    class Meta:
        model=Bug
        fields = '__all__'
        # fields = ['file_odb']

class BugFormsReadOnly(forms.ModelForm):
    """
    Meta : 该类是必须继承的,但是该字段是
    model :对应的模型类
    fields : 当为‘__all__就是验证全部字段’,当只想验证其中部分的字段的时候，需要使用[]包裹起来
    """
    class Meta:
        model = Bug
        fields = '__all__'


        def __init__(self, *args, **kwargs):
            super(BugFormsReadOnly, self).__init__(*args, **kwargs)
            for name, field in self.fields.iteritems():
                field.widget.attrs['readonly'] = 'true'
