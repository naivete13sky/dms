from django.contrib import admin
from .models import Profile,FactoryRule,CustomerRule

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile','recommender','cam_level','date_of_birth', 'photo']

@admin.register(FactoryRule)
class FactoryRuleAdmin(admin.ModelAdmin):
    list_display = ['factory_rule_name','remark' ,'author']

@admin.register(CustomerRule)
class CustomerRuleAdmin(admin.ModelAdmin):
    list_display = ['customer_rule_name','remark' ,'author']