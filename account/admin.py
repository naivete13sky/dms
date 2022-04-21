from django.contrib import admin
from .models import Profile,FactoryRule

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile','recommender','cam_level','date_of_birth', 'photo']

@admin.register(FactoryRule)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['factory_rule_name', ]