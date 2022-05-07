from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'order'
urlpatterns = [
    path('',views.CamOrderListView.as_view(),name='index'),
    path('CamOrderListView',views.CamOrderListView.as_view(),name='CamOrderListView'),
    re_path('CamOrderFormView/(?P<parm>\w+)/', views.CamOrderFormView.as_view(), name='CamOrderFormView'),
    path('CamOrderCreateView', views.CamOrderCreateView.as_view(), name='CamOrderCreateView'),
    path('CamOrderUpdateView/<int:pk>', views.CamOrderUpdateView.as_view(), name='CamOrderUpdateView'),
    path('CamOrderDeleteView/<int:pk>', views.CamOrderDeleteView.as_view(),name='CamOrderDeleteView'),
    # path('project_settings', views.project_settings, name='project_settings'),

    path('CamOrderProcessListView',views.CamOrderProcessListView.as_view(),name='CamOrderProcessListView'),
    re_path('CamOrderProcessFormView/(?P<parm>\w+)/', views.CamOrderProcessFormView.as_view(), name='CamOrderProcessFormView'),
    path('CamOrderProcessCreateView', views.CamOrderProcessCreateView.as_view(), name='CamOrderProcessCreateView'),
    path('CamOrderProcessUpdateView/<int:pk>', views.CamOrderProcessUpdateView.as_view(), name='CamOrderProcessUpdateView'),
    path('CamOrderProcessDeleteView/<int:pk>', views.CamOrderProcessDeleteView.as_view(),name='CamOrderProcessDeleteView'),


    path('input_status_select',views.input_status_select,name='input_status_select'),




# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)