from django.contrib import admin
from .models import CamOrder
# Register your models here.
@admin.register(CamOrder)
class CamOrderAdmin(admin.ModelAdmin):
    list_display = ('name','remark','project','customer_user','customer_price','process_user','process_price',
                    'author','status','process_times','publish',
                    'last_update_user','cam_order_type')
    search_fields = ('name','project','customer_user','process_user','author')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10