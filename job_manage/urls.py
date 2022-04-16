from django.urls import path
from . import views

app_name = 'job_manage'
urlpatterns = [
    # post views
    # path("order_view/", views.list_all_job, name='order_view'),
    # path("admin/order_view/", views.list_all_job, name='order_view'),
    path('job_upload', views.job_upload, name='job_upload'),
    path('job_upload_ajax', views.job_upload_ajax, name='job_upload_ajax'),


]