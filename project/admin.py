from django.contrib import admin
from .models import Project
# Register your models here.
admin.site.site_header = 'CAM料号管理系统'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','org','work','author','publish')
    search_fields = ('name','org','work','author','publish')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10