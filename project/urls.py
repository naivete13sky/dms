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
    # path('factoryrule_create', views.FactoryRuleCreateView.as_view(), name='factoryrule_create'),
    # path('factoryrule_update/<int:pk>', views.FactoryRuleUpdateView.as_view(), name='factoryrule_update'),
    # path('factoryrule_delete/<int:pk>', views.FactoryRuleDeleteView.as_view(),name='factoryrule_delete'),




# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)