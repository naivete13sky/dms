from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# admin.site.register(Order)

from django.contrib import admin
from .models import Job,ShareAccount,Layer
# from .views import list_all_job
admin.site.site_header = 'CAM料号管理系统'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name','file_odb','file_compressed','file_odb_current','file_odb_g','vs_result_ep','vs_result_g','author','from_object',)

    search_fields = ('job_name','author__username',)
    prepopulated_fields = {'remark': ('job_name',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(ShareAccount)
class ShareAccountAdmin(admin.ModelAdmin):
    list_display = ('share_job','share_account','remark',)
    list_filter = ('share_job','share_account','remark',)
    search_fields = ('share_job','share_account','remark',)
    # prepopulated_fields = {'slug': ('share_account',)}
    raw_id_fields = ('share_account',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ('job','layer','layer_org','layer_file_type','layer_type','drill_excellon2_units','drill_excellon2_zeroes_omitted','drill_excellon2_number_format_A','drill_excellon2_number_format_B','drill_excellon2_tool_units',)

    search_fields = ('job','layer','layer_file_type','layer_type')
    prepopulated_fields = {'remark': ('layer',)}
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10