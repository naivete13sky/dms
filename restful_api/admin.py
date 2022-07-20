from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tutorial
# Register your models here.
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title','description','published')
    search_fields = ('title','description','published')
    # raw_id_fields = ('author',)
    # date_hierarchy = 'published'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10
