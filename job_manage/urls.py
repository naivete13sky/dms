from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'job_manage'
urlpatterns = [
    # post views
    # path("order_view/", views.list_all_job, name='order_view'),
    # path("admin/order_view/", views.list_all_job, name='order_view'),
    path('job_upload', views.job_upload, name='job_upload'),
    path('job_upload_ajax', views.job_upload_ajax, name='job_upload_ajax'),
    path('reg/', views.reg,name='reg'),
    re_path('job/$', views.JobAdd),
    re_path('job/(?P<id>\d+)/$', views.JobEdit),
    path('', views.AddArticle.as_view()),
    path('register/', views.RegisterArticle.as_view()),
    path('uploadcc/', views.UploadFiles.as_view()),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)