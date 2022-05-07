from django.contrib import admin
from .models import CamOrder,CamOrderProcess
# Register your models here.
@admin.register(CamOrder)
class CamOrderAdmin(admin.ModelAdmin):
    list_display = ('name','remark','project','customer_user','customer_price','should_finish_time','process_user','process_price',
                    'author','status','process_times','publish',
                    'last_update_user','cam_order_type')
    search_fields = ('name','project','customer_user','should_finish_time','process_user','author')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(CamOrderProcess)
class CamOrderProcessAdmin(admin.ModelAdmin):
    list_display = ('name','remark','cam_order','data','author','publish')
    search_fields = ('name','remark','cam_order','data','author','publish')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10