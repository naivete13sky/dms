from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'job_manage'
urlpatterns = [
    # post views
    # path("order_view/", views.list_all_job, name='order_view'),
    # path("admin/order_view/", views.list_all_job, name='order_view'),
    # path('job_upload', views.job_upload, name='job_upload'),
    path('job_upload_ajax', views.job_upload_ajax, name='job_upload_ajax'),
    path('reg/', views.reg,name='reg'),
    # re_path('job/$', views.JobAdd),
    re_path('job/(?P<id>\d+)/$', views.Edit,name='edit'),
    # re_path('upload/$', views.JobUpload.as_view(), name='upload'),
    path('addArticle', views.AddArticle.as_view()),
    path('register/', views.RegisterArticle.as_view()),
    # path('uploadcc/', views.UploadFiles.as_view()),
    # path('', views.job_view,name='job_view'),
    # path('add', views.JobUpload.as_view(), name='add'),
    path('add', views.add, name='add'),
    path('add2', views.add,name='add2'),#附件有问题
    path('',views.JobListView.as_view(),name='job_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:job>/', views.job_detail, name='job_detail'),
    path('view',views.job_view,name='job_view'),

# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)