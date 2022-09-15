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
    fields = ('name_full','name_simple','department','customer_type', ('country', 'province', 'city'))

    list_display = ['name_full', 'name_simple', 'department','province','city', 'customer_type', 'remark']

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

    def get_region_dict(self):
        region_dict={}
        region_dict_china = {}
        data = json.load(open(os.path.join(settings.BASE_DIR,r'account\china_region.json')))
        data_version = data['data_version']
        provinces = data['result'][0]
        citys = data['result'][1]
        for province in provinces:
            pass
            # print(province["fullname"])

            cidx = province['cidx']
            province_citys_js = citys[cidx[0]:cidx[1]]
            one_province_city_list = []
            for city in province_citys_js:
                pass
                # print(city["fullname"])
                one_province_city_list.append(city["fullname"])
            region_dict_china[province["fullname"]] = one_province_city_list

        region_dict["中国"]=region_dict_china
        region_dict["国外"]={'亚洲': ['日本','韩国','朝鲜'],
                  '欧洲': ['英国','德国','法国','瑞士'],
                  '非洲': ['南非','埃及','加纳','贝宁','苏丹','中非'],
                  '美洲': ['美国','巴西','智利','古巴','海地','秘鲁'],
                  '大洋洲': ['帕劳','斐济','汤加','纽埃','瑙鲁','萨摩亚']}
        return region_dict

    #重写add_view方法是为了实现把区域信息传给change_form.html页面中。
    def add_view(self, request,  extra_context=None):
        extra_context = extra_context or {}
        extra_context['region_dict'] = self.get_region_dict()

        return super(CustomerAdmin, self).add_view(
            request,extra_context=extra_context,
        )
