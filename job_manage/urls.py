from django.contrib.auth.decorators import login_required
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
    path('JobListView',login_required(views.JobListView.as_view()),name='JobListView'),
    path('JobListViewVs',login_required(views.JobListViewVs.as_view()),name='JobListViewVs'),
    re_path('detail/(?P<pk>\d+)/', login_required(views.JobDetailView.as_view()), name='detail'),
    re_path('JobFormView/(?P<parm>\w+)/', login_required(views.JobFormView.as_view()), name='JobFormView'),
    re_path('form/(?P<parm>\w+)/', login_required(views.JobFormView.as_view()), name='form'),
    path('tag/<slug:tag_slug>/', views.job_list, name='job_list_by_tag'),
    path('add', views.add, name='add'),
    path('<int:year>/<int:month>/<int:day>/<slug:job>/', views.job_detail, name='job_detail'),
    path('',login_required(views.JobListView.as_view()),name='job_view'),
    path('del_job/<int:job_id>/', views.del_job, name='del_job'),
    path('share_job/<int:job_id>/', views.share_job, name='share_job'),
    path('job_analysis', views.job_analysis, name='job_analysis'),
    path('JobCreateView', views.JobCreateView.as_view(), name='JobCreateView'),
    path('job_settings', views.job_settings, name='job_settings'),
    path('JobUpdateView/<int:pk>', views.JobUpdateView.as_view(), name='JobUpdateView'),
    path('JobUpdateViewVs/<int:pk>', views.JobUpdateViewVs.as_view(), name='JobUpdateViewVs'),
    path('JobDeleteView/<int:pk>', views.JobDeleteView.as_view(),name='JobDeleteView'),
    path('gerber274x_to_odb_ep/<int:job_id>/', views.gerber274x_to_odb_ep,name='gerber274x_to_odb_ep'),

    path('LayerListView',login_required(views.LayerListView.as_view()),name='LayerListView'),
    path('view_layer/<int:job_id>/', views.view_layer,name='view_layer'),
    path('get_file_name_from_org/<int:job_id>/', views.get_file_name_from_org,name='get_file_name_from_org'),
    path('LayerUpdateView/<int:pk>', views.LayerUpdateView.as_view(), name='LayerUpdateView'),
    path('LayerUpdateViewOneJob/<int:pk>', views.LayerUpdateViewOneJob.as_view(), name='LayerUpdateViewOneJob'),



# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)