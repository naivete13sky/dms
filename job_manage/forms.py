from django import forms
from django.forms import widgets
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