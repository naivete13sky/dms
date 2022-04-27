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




# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)