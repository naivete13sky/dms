from django.urls import path
from . import views

app_name = 'back_stage'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('index_base_20220818', views.index_base_20220818, name='index_base_20220818'),


]