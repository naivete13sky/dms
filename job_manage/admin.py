from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# admin.site.register(Order)

from django.contrib import admin
from .models import Job,Article
# from .views import list_all_job

admin.site.site_header = 'CAM料号管理系统'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name','file_odb', 'slug', 'receive_staff', 'receive_date', 'recipe_status')
    list_filter = ('recipe_status', 'receive_date', 'receive_staff',)
    search_fields = ('job_name', 'receive_staff',)
    prepopulated_fields = {'slug': ('job_name',)}
    # raw_id_fields = ('receive_staff',)
    date_hierarchy = 'receive_date'
    ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','content','author',)
    list_filter = ('title','content','author',)
    search_fields = ('title','content','author',)
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('receive_staff',)
    date_hierarchy = 'create_time'
    ordering = ('create_time', )
    list_per_page = 10