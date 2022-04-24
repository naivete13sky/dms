from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# admin.site.register(Order)

from django.contrib import admin
from .models import Job,ShareAccount
# from .views import list_all_job
admin.site.site_header = 'CAM料号管理系统'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name','file_odb','file_compressed','author',)
    search_fields = ('job_name','author__username',)
    prepopulated_fields = {'slug': ('job_name',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(ShareAccount)
class ShareAccountAdmin(admin.ModelAdmin):
    list_display = ('share_job','share_account','remark',)
    list_filter = ('share_job','share_account','remark',)
    search_fields = ('share_job','share_account','remark',)
    prepopulated_fields = {'slug': ('share_account',)}
    raw_id_fields = ('share_account',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10


