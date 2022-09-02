from django.contrib import admin
from .models import Profile,FactoryRule,CustomerRule,QueryData

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