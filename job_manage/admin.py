from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# admin.site.register(Order)

from django.contrib import admin
from .models import Job
# from .views import list_all_job
admin.site.site_header = 'CAM料号管理系统'

@admin.register(Job)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','content','author',)
    list_filter = ('title','content','author',)
    search_fields = ('title','content','author',)
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('receive_staff',)
    # date_hierarchy = 'receive_date'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10