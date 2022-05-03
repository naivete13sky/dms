from django.contrib import admin
from .models import Carriage,Train,TrainSet
# Register your models here.
@admin.register(Carriage)
class CarriageAdmin(admin.ModelAdmin):
    list_display = ('name','remark','carriage_type','carriage_use','author_exe','check_set','author_check',
                    'author_create','publish')
    search_fields = ('name','carriage_type','carriage_use','author_create')
    raw_id_fields = ('author_create',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name','remark','train_use','train_author_create','publish',)
    search_fields = ('name','remark','train_use','train_author_create','publish',)
    raw_id_fields = ('train_author_create',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10

@admin.register(TrainSet)
class TrainSetAdmin(admin.ModelAdmin):
    list_display = ('name','remark','order_id','train','current_carriage','pre_carriage','post_carriage','current_carriage_author_create',)
    search_fields = ('name','remark','train','current_carriage','pre_carriage','post_carriage','current_carriage_author_create',)
    raw_id_fields = ('current_carriage_author_create',)
    date_hierarchy = 'publish'
    # ordering = ('recipe_status', 'receive_date',)
    list_per_page = 10