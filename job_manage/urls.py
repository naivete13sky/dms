from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'job_manage'
urlpatterns = [
    path('reg/', views.reg,name='reg'),#函数视图，自己写的，供研究注册表单填写与校验用。
    re_path('job/(?P<id>\d+)/$', views.Edit,name='edit'),#函数视图，自己写的修改Job。
    path('addArticle', views.AddArticle.as_view()),#函数视图，自己写的新增Job.
    path('register/', views.RegisterArticle.as_view()),#自己写的注册用户，是register这张表，这是研究用的。实际上dms没有用这个注册功能。
    path('job_list', views.job_list,name='job_list'),#自己写的函数视图，查看料号列表，筛选了published状态的。实际上dms不需要这个。


    path('JobListViewInput',login_required(views.JobListViewInput.as_view()),name='JobListViewInput'),#类视图，测试组用来测试料号导出的，目前dms默认打开的就是这个页面。
    path('JobListView2',login_required(views.JobListView2.as_view()),name='JobListView2'),#类视图，研究用的。目前这个视图在dms中没用上。
    path('JobListViewJquery',login_required(views.JobListViewJquery.as_view()),name='JobListViewJquery'),#类视图，研究前端用Jquery的DataTable插件用的，感觉没有django的模板好用。目前这个视图在dms中没用上。
    path('JobListView',login_required(views.JobListView.as_view()),name='JobListView'),#类视图，用来组普通用户展示料号列表的。
    re_path('detail/(?P<pk>\d+)/', login_required(views.JobDetailView.as_view()), name='detail'),#类视图DetailView，用来查看料号详细信息的。dms中没有用这个函数视图，用了类视图JobFormView。
    re_path('JobFormView/(?P<parm>\w+)/', login_required(views.JobFormView.as_view()), name='JobFormView'),#类视图，多用了ModelForm，查看某相料号的详细信息。其实还是DetailView省事。
    # path('tag/<slug:tag_slug>/', views.job_list, name='job_list_by_tag'),#原来查看tag的，为了增加tag支持中文，修改了url。不用<slug：，只能用<str:了。
    # 这里的参数类型不要写slug，否则又会忽视中文，写str就行了
    path('tag/<str:tag_slug>/', views.job_list, name='job_list_by_tag'),
    path('add', views.add, name='add'),#函数视图，一开始用来新增料号的，后来增加了好多字段，没有继续维护更新。供研究用吧。dms中通过CreatView来新增料号的。
    path('<int:year>/<int:month>/<int:day>/<slug:job>/', views.job_detail, name='job_detail'),#函数视图，用来查看料号详细信息的。dms中没用这个。
    path('',login_required(views.JobListView.as_view()),name='job_view'),#job_manage 这个app下，默认路由指向。
    path('del_job/<int:job_id>/', views.del_job, name='del_job'),#函数视图，用来删除料号的。也可能通过DeleteView来实现，目前都在用，其实可以只用后者的。
    path('share_job/<int:job_id>/', views.share_job, name='share_job'),#函数视频，用来分享料号的。
    path('job_analysis', views.job_analysis, name='job_analysis'),#函数视图，用来分析料号的，具体功能还未实现。
    path('JobCreateView', views.JobCreateView.as_view(), name='JobCreateView'),#类视图，新增料号。
    path('job_settings', views.job_settings, name='job_settings'),#函数视图，用来设置料号比对参数用的。
    path('JobUpdateView/<int:pk>/<int:current_page>', views.JobUpdateView.as_view(), name='JobUpdateView'),#类视图，用来更新料号的。
    path('JobUpdateViewVs/<int:pk>', views.JobUpdateViewVs.as_view(), name='JobUpdateViewVs'),#类视图，现在没有用这个。与VS交互的逻辑已经在JobUpdateView里都实现了。
    path('JobDeleteView/<int:pk>', views.JobDeleteView.as_view(),name='JobDeleteView'),#类视图，删除料号。
    path('gerber274x_to_odb_ep/<int:job_id>/', views.gerber274x_to_odb_ep,name='gerber274x_to_odb_ep'),#悦谱转图，已经不用了。
    path('gerber274x_to_odb_ep2/<int:job_id>/<int:current_page>', views.gerber274x_to_odb_ep2,name='gerber274x_to_odb_ep2'),#悦谱转图。
    path('gerber274x_to_odb_g/<int:job_id>/', views.gerber274x_to_odb_g,name='gerber274x_to_odb_g'),#G转图
    path('ep_current_odb_view/<int:job_id>/<int:current_page>', views.ep_current_odb_view,name='ep_current_odb_view'),#查看悦谱最新转图的料号
    path('g_current_odb_view/<int:job_id>/<int:current_page>', views.g_current_odb_view,name='g_current_odb_view'),#查看G转图的料号。

    path('LayerListView',login_required(views.LayerListView.as_view()),name='LayerListView'),#层信息列表

    path('LayerListViewPara',login_required(views.LayerListViewPara.as_view()),name='LayerListViewPara'),#层信息列表


    path('view_layer/<int:job_id>/', views.view_layer,name='view_layer'),#查看某个料号下的层信息，其实这个可以不用了。LayerListView已经支持只看某个料的层信息了。
    path('layer_set_vs_result_manual', views.layer_set_vs_result_manual,name='layer_set_vs_result_manual'),#这个功能 忘记了，要再研究一下!!!!!!!!!!!!!

    path('get_file_name_from_org/<int:job_id>/', views.get_file_name_from_org,name='get_file_name_from_org'),#根据整理过的gerber压缩包，生成层别信息。
    path('get_file_name_from_org_on/<int:job_id>/', views.get_file_name_from_org_on,name='get_file_name_from_org_on'),#打开生成层别名称的入口开关。之前有过这样，对于已有层别信息的料，隐藏生成层别信息的的入口，防止新生成的把原来的老信息都边覆盖了。
    path('delete_all_layer_info/<int:job_id>/', views.delete_all_layer_info,name='delete_all_layer_info'),#删除某个料号下的所有层别信息，这个功能比较危险，后来没有在页面提供入口。
    path('LayerUpdateView/<int:pk>', views.LayerUpdateView.as_view(), name='LayerUpdateView'),#更新层别信息。
    path('LayerUpdateViewOneJob/<int:pk>', views.LayerUpdateViewOneJob.as_view(), name='LayerUpdateViewOneJob'),#更新层别信息，一开始为了与某个料号有交互才这样写的，后来LayerUpdateView已经支持了与某个料号的交互。
    re_path('LayerFormView/(?P<parm>\w+)/', views.LayerFormView.as_view(), name='LayerFormView'),#查看层别详细

    path('vs_ep/<int:job_id>/<int:current_page>', views.vs_ep,name='vs_ep'),#悦谱比图
    path('vs_g/<int:job_id>/<int:current_page>', views.vs_g,name='vs_g'),#G比图

    path('VsListView',login_required(views.VsListView.as_view()),name='VsListView'),#比图结果的列表
    path('view_vs_ep/<int:job_id>/', views.view_vs_ep,name='view_vs_ep'),#查看悦谱比图列表
    path('view_vs_g/<int:job_id>/', views.view_vs_g,name='view_vs_g'),#查看G比图的列表
    path('view_vs_one_layer/<int:job_id>/<str:layer_org>/', views.view_vs_one_layer,name='view_vs_one_layer'),#查看某个料号下的比图信息

    path('BugListView',login_required(views.BugListView.as_view()),name='BugListView'),#Bug列表
    path('BugCreateView', views.BugCreateView.as_view(), name='BugCreateView'),#新增Bug，只要写个神道ID就行了。
    path('BugUpdateView/<int:pk>', views.BugUpdateView.as_view(), name='BugUpdateView'),#更新Bug,其实就是更新Bug ID才有意义，其他信息在禅道中更新就好了。
    re_path('BugFormView/(?P<parm>\w+)/', login_required(views.BugFormView.as_view()), name='BugFormView'),#查看Bug详细，其实用DetailView写更省事。
    path('BugDeleteView/<int:pk>', views.BugDeleteView.as_view(),name='BugDeleteView'),#删除Bug。
    path('refresh_bug_info/<int:job_id>/', views.refresh_bug_info,name='refresh_bug_info'),#刷新Bug状态，就是重新从禅道拉信息同步过来。

    path('send_vs_g_local_result', views.send_vs_g_local_result,name='send_vs_g_local_result'),#开发时测试用的。





    path('test', views.test,name='test'),#开发时测试用的。
    path('test_text_input_same_auto', views.test_text_input_same_auto,name='test_text_input_same_auto'),
    path('test_ajax_index', views.test_ajax_index,name='test_ajax_index'),
    path('test_ajax_add/', views.test_ajax_add,name='test_ajax_add'),
    path('test_ajax_add2/', views.test_ajax_add2,name='test_ajax_add2'),
    path('test_ajax_checkbox/', views.test_ajax_checkbox,name='test_ajax_checkbox'),#not ok,没有提交代码
    path('test_ajax_checkbox2/', views.test_ajax_checkbox2,name='test_ajax_checkbox2'),
    path('test_ajax_checkbox3/', views.test_ajax_checkbox3,name='test_ajax_checkbox3'),
    path('test_ajax_checkbox4/', views.test_ajax_checkbox4,name='test_ajax_checkbox4'),
    path('test_ajax_checkbox5/', views.test_ajax_checkbox5,name='test_ajax_checkbox5'),
    path('test_ajax_post1/', views.test_ajax_post1,name='test_ajax_post1'),#not ok
    path('test_ajax_HttpResponse/', views.test_ajax_HttpResponse,name='test_ajax_HttpResponse'),
    path('test_ajax_HttpResponse_json/', views.test_ajax_HttpResponse_json,name='test_ajax_HttpResponse_json'),
    path('test_ajax_JsonResponse_json/', views.test_ajax_JsonResponse_json,name='test_ajax_JsonResponse_json'),
    path('test_ajax_HttpResponse_front_not_Deserialization/', views.test_ajax_HttpResponse_front_not_Deserialization,name='test_ajax_HttpResponse_front_not_Deserialization'),
    #在和form表单一块用的时候,form表单里不能写button 和input type="submit",因为在form表单里都是提交，和ajax一块用时form提交一次，ajax再提交一次，就会有问题。所以在form表单中使用<input type='button'>, 要么不用form表单
    path('test_ajax_post/', views.test_ajax_post,name='test_ajax_post'),
    path('test_ajax_upload/', views.test_ajax_upload,name='test_ajax_upload'),
    path('test_casbin/', views.test_casbin,name='test_casbin'),
    path('temp', views.temp,name='temp'),
    path('test_js_local_script', views.test_js_local_script, name='test_js_local_script'),  # js调用cmd
    path('test_js_local_script2', views.test_js_local_script2, name='test_js_local_script2'),  # js调用python，pyscript
    path('tag_cloud', views.tag_cloud,name='tag_cloud'),#标签云

# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)