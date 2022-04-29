from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'project'
urlpatterns = [
    path('',views.ProjectListView.as_view(),name='index'),
    path('ProjectListView',views.ProjectListView.as_view(),name='ProjectListView'),
    re_path('ProjectFormView/(?P<parm>\w+)/', views.ProjectFormView.as_view(), name='ProjectFormView'),
    path('ProjectCreateView', views.ProjectCreateView.as_view(), name='ProjectCreateView'),
    path('ProjectUpdateView/<int:pk>', views.ProjectUpdateView.as_view(), name='ProjectUpdateView'),
    path('ProjectDeleteView/<int:pk>', views.ProjectDeleteView.as_view(),name='ProjectDeleteView'),
    path('project_settings', views.project_settings, name='project_settings'),

    path('factory_rule_delete/<int:pk>', views.factory_rule_delete,name='factory_rule_delete'),
    path('factory_rule_select/<int:author_id>/<int:id>', views.factory_rule_select,name='factory_rule_select'),
    path('factory_rule_new/<int:author_id>/<int:id>', views.factory_rule_new,name='factory_rule_new'),



# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)