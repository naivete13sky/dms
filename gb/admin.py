from django.contrib import admin
from .models import Org,Pre

@admin.register(Org)
class PostAdmin(admin.ModelAdmin):
    list_display = ('company_name','job_name_org','file_org', 'slug', 'receive_staff', 'receive_date', 'recipe_status')
    list_filter = ('company_name','recipe_status', 'receive_date', 'receive_staff',)
    search_fields = ('company_name','job_name_org', 'receive_staff',)
    prepopulated_fields = {'slug': ('job_name_org',)}
    # raw_id_fields = ('receive_staff',)
    date_hierarchy = 'receive_date'
    ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(Pre)
class Order_pre_Admin(admin.ModelAdmin):
    list_display = ('job_name_pre','file_pre', 'slug', 'pre_staff', 'pre_date', 'pre_status')
    list_filter = ('pre_status', 'pre_date', 'pre_staff',)
    search_fields = ('job_name_pre', 'pre_staff',)
    prepopulated_fields = {'slug': ('job_name_pre',)}
    # raw_id_fields = ('pre_staff',)
    date_hierarchy = 'pre_date'
    ordering = ('pre_status', 'pre_date',)
    list_per_page = 10