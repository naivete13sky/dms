from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'job_manage'
urlpatterns = [
    path('job_upload_ajax', views.job_upload_ajax, name='job_upload_ajax'),
    path('reg/', views.reg,name='reg'),
    re_path('job/(?P<id>\d+)/$', views.Edit,name='edit'),
    path('addArticle', views.AddArticle.as_view()),
    path('register/', views.RegisterArticle.as_view()),
    path('job_list', views.job_list,name='job_list'),
    path('JobListView',views.JobListView.as_view(),name='JobListView'),
    re_path('detail/(?P<pk>\d+)/', views.JobDetailView.as_view(), name='detail'),
    re_path('form/(?P<parm>\w+)/', views.JobFormView.as_view(), name='form'),
    path('tag/<slug:tag_slug>/', views.job_list, name='job_list_by_tag'),
    path('add', views.add, name='add'),
    path('<int:year>/<int:month>/<int:day>/<slug:job>/', views.job_detail, name='job_detail'),
    path('',views.job_view,name='job_view'),
    path('del_job/<int:job_id>/', views.del_job, name='del_job'),
    path('share_job/<int:job_id>/', views.share_job, name='share_job'),



# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)