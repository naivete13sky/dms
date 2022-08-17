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
    # path('JobListView',login_required(views.JobListView.as_view()),name='JobListView'),
    #暂时先改为JobListViewVs，平时是JobListView
    path('JobListView',login_required(views.JobListView.as_view()),name='JobListView'),
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
    path('gerber274x_to_odb_ep2/<int:job_id>/', views.gerber274x_to_odb_ep2,name='gerber274x_to_odb_ep2'),
    path('gerber274x_to_odb_g/<int:job_id>/', views.gerber274x_to_odb_g,name='gerber274x_to_odb_g'),

    path('LayerListView',login_required(views.LayerListView.as_view()),name='LayerListView'),
    path('view_layer/<int:job_id>/', views.view_layer,name='view_layer'),
    path('layer_set_vs_result_manual', views.layer_set_vs_result_manual,name='layer_set_vs_result_manual'),

    path('get_file_name_from_org/<int:job_id>/', views.get_file_name_from_org,name='get_file_name_from_org'),
    path('get_file_name_from_org_on/<int:job_id>/', views.get_file_name_from_org_on,name='get_file_name_from_org_on'),
    path('delete_all_layer_info/<int:job_id>/', views.delete_all_layer_info,name='delete_all_layer_info'),
    path('LayerUpdateView/<int:pk>', views.LayerUpdateView.as_view(), name='LayerUpdateView'),
    path('LayerUpdateViewOneJob/<int:pk>', views.LayerUpdateViewOneJob.as_view(), name='LayerUpdateViewOneJob'),
    re_path('LayerFormView/(?P<parm>\w+)/', views.LayerFormView.as_view(), name='LayerFormView'),

    path('vs_ep/<int:job_id>/', views.vs_ep,name='vs_ep'),
    path('vs_g/<int:job_id>/', views.vs_g,name='vs_g'),

    path('VsListView',login_required(views.VsListView.as_view()),name='VsListView'),
    path('view_vs_ep/<int:job_id>/', views.view_vs_ep,name='view_vs_ep'),
    path('view_vs_g/<int:job_id>/', views.view_vs_g,name='view_vs_g'),
    path('view_vs_one_layer/<int:job_id>/<str:layer_org>/', views.view_vs_one_layer,name='view_vs_one_layer'),

    path('BugListView',login_required(views.BugListView.as_view()),name='BugListView'),
    path('BugCreateView', views.BugCreateView.as_view(), name='BugCreateView'),
    path('BugUpdateView/<int:pk>', views.BugUpdateView.as_view(), name='BugUpdateView'),
    re_path('BugFormView/(?P<parm>\w+)/', login_required(views.BugFormView.as_view()), name='BugFormView'),
    path('BugDeleteView/<int:pk>', views.BugDeleteView.as_view(),name='BugDeleteView'),
    path('refresh_bug_info/<int:job_id>/', views.refresh_bug_info,name='refresh_bug_info'),



    path('test', views.test,name='test'),
    path('test_ajax_index', views.test_ajax_index,name='test_ajax_index'),
    path('test_ajax_add/', views.test_ajax_add,name='test_ajax_add'),
    path('test_ajax_add2/', views.test_ajax_add2,name='test_ajax_add2'),
    path('test_ajax_checkbox/', views.test_ajax_checkbox,name='test_ajax_checkbox'),#not ok,没有提交代码
    path('test_ajax_checkbox2/', views.test_ajax_checkbox2,name='test_ajax_checkbox2'),
    path('test_ajax_checkbox3/', views.test_ajax_checkbox3,name='test_ajax_checkbox3'),
    path('test_ajax_checkbox4/', views.test_ajax_checkbox4,name='test_ajax_checkbox4'),
    path('test_ajax_post1/', views.test_ajax_post1,name='test_ajax_post1'),#not ok
    path('test_ajax_HttpResponse/', views.test_ajax_HttpResponse,name='test_ajax_HttpResponse'),
    path('test_ajax_HttpResponse_json/', views.test_ajax_HttpResponse_json,name='test_ajax_HttpResponse_json'),
    path('test_ajax_JsonResponse_json/', views.test_ajax_JsonResponse_json,name='test_ajax_JsonResponse_json'),
    path('test_ajax_HttpResponse_front_not_Deserialization/', views.test_ajax_HttpResponse_front_not_Deserialization,name='test_ajax_HttpResponse_front_not_Deserialization'),
    #在和form表单一块用的时候,form表单里不能写button 和input type="submit",因为在form表单里都是提交，和ajax一块用时form提交一次，ajax再提交一次，就会有问题。所以在form表单中使用<input type='button'>, 要么不用form表单
    path('test_ajax_post/', views.test_ajax_post,name='test_ajax_post'),
    path('test_ajax_upload/', views.test_ajax_upload,name='test_ajax_upload'),


# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)