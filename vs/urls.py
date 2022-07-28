from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'vs'
urlpatterns = [
    path('',views.ProjectListView.as_view(),name='index'),
    path('VsListView',views.VsListView.as_view(),name='VsListView'),
    # re_path('ProjectFormView/(?P<parm>\w+)/', views.ProjectFormView.as_view(), name='ProjectFormView'),
    # path('ProjectCreateView', views.ProjectCreateView.as_view(), name='ProjectCreateView'),
    # path('ProjectUpdateView/<int:pk>', views.ProjectUpdateView.as_view(), name='ProjectUpdateView'),
    # path('ProjectDeleteView/<int:pk>', views.ProjectDeleteView.as_view(),name='ProjectDeleteView'),
    # path('ProjectUploadWork/<int:pk>', views.ProjectUploadWork.as_view(), name='ProjectUploadWork'),
    # path('project_upload_work/<int:pk>', views.project_upload_work, name='project_upload_work'),
    # path('project_settings', views.project_settings, name='project_settings'),

    # path('factory_rule_delete/<int:pk>', views.factory_rule_delete,name='factory_rule_delete'),
    # path('factory_rule_select/<int:author_id>/<int:id>', views.factory_rule_select,name='factory_rule_select'),
    # path('factory_rule_new/<int:author_id>/<int:id>', views.factory_rule_new,name='factory_rule_new'),
    # path('FactoryRuleListView',views.FactoryRuleListView.as_view(),name='FactoryRuleListView'),
    # re_path('FactoryRuleFormView/(?P<parm>\w+)/', views.FactoryRuleFormView.as_view(), name='FactoryRuleFormView'),
    # path('FactoryRuleCreateView', views.FactoryRuleCreateView.as_view(), name='FactoryRuleCreateView'),
    # path('FactoryRuleUpdateView/<int:pk>', views.FactoryRuleUpdateView.as_view(), name='FactoryRuleUpdateView'),
    # path('FactoryRuleDeleteView/<int:pk>', views.FactoryRuleDeleteView.as_view(),name='FactoryRuleDeleteView'),
    #
    # path('customer_rule_delete/<int:pk>', views.customer_rule_delete,name='customer_rule_delete'),
    # path('customer_rule_select/<int:author_id>/<int:id>', views.customer_rule_select,name='customer_rule_select'),
    # path('customer_rule_new/<int:author_id>/<int:id>', views.customer_rule_new,name='customer_rule_new'),
    # path('CustomerRuleListView',views.CustomerRuleListView.as_view(),name='CustomerRuleListView'),
    # re_path('CustomerRuleFormView/(?P<parm>\w+)/', views.CustomerRuleFormView.as_view(), name='CustomerRuleFormView'),
    # path('CustomerRuleCreateView', views.CustomerRuleCreateView.as_view(), name='CustomerRuleCreateView'),
    # path('CustomerRuleUpdateView/<int:pk>', views.CustomerRuleUpdateView.as_view(), name='CustomerRuleUpdateView'),
    # path('CustomerRuleDeleteView/<int:pk>', views.CustomerRuleDeleteView.as_view(),name='CustomerRuleDeleteView'),




# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)