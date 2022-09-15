from django.contrib import admin
from .models import Profile,FactoryRule,CustomerRule,QueryData,Customer
from django import forms
import json
import os
from django.conf import settings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile','recommender','cam_level','date_of_birth', 'photo']

@admin.register(FactoryRule)
class FactoryRuleAdmin(admin.ModelAdmin):
    list_display = ['factory_rule_name','remark' ,'author']

@admin.register(CustomerRule)
class CustomerRuleAdmin(admin.ModelAdmin):
    list_display = ['customer_rule_name','remark' ,'author']


@admin.register(QueryData)
class QueryDataAdmin(admin.ModelAdmin):
    list_display = ['query_job_file_usage_type','query_job_job_name','query_job_author','query_job_from_object','remark' ,'author']


class CustomerForm(forms.ModelForm):
    class Meta:
        widgets = {
            'country': forms.Select(),
            'province': forms.Select(),
            'city': forms.Select(),
        }

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    form = CustomerForm
    fields = ('name', ('country', 'province', 'city'))

    list_display = ['name_full', 'name_simple', 'department', 'province0', 'city', 'customer_type', 'remark']

    def get_province_tuple(self):
        pass
        data = json.load(open(os.path.join(settings.BASE_DIR,r'account\china_region.json')))
        data_version = data['data_version']
        provinces = data['result'][0]
        provinces_tuple = ()
        for province in provinces:
            pass
            # print(province)
            # print(province["fullname"])
            provinces_tuple = provinces_tuple + ((province["id"], province["fullname"]),)
        print(provinces_tuple)
        # print(type(provinces_tuple))
        return provinces_tuple

    def add_view(self, request,  extra_context=None):
        extra_context = extra_context or {}
        extra_context['cc'] = self.get_province_tuple()

        return super(CustomerAdmin, self).add_view(
            request,extra_context=extra_context,
        )
