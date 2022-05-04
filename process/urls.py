from django.contrib.auth.decorators import login_required
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'process'
urlpatterns = [
    # path('',views.CamOrderListView.as_view(),name='index'),
    path('CarriageListView',views.CarriageListView.as_view(),name='CarriageListView'),
    re_path('CarriageFormView/(?P<parm>\w+)/', views.CarriageFormView.as_view(), name='CarriageFormView'),
    path('CarriageCreateView', views.CarriageCreateView.as_view(), name='CarriageCreateView'),
    path('CarriageUpdateView/<int:pk>', views.CarriageUpdateView.as_view(), name='CarriageUpdateView'),
    path('CarriageDeleteView/<int:pk>', views.CarriageDeleteView.as_view(),name='CarriageDeleteView'),
    # path('project_settings', views.project_settings, name='project_settings'),

    path('TrainListView',views.TrainListView.as_view(),name='TrainListView'),
    re_path('TrainFormView/(?P<parm>\w+)/', views.TrainFormView.as_view(), name='TrainFormView'),
    path('TrainCreateView', views.TrainCreateView.as_view(), name='TrainCreateView'),
    path('TrainUpdateView/<int:pk>', views.TrainUpdateView.as_view(), name='TrainUpdateView'),
    path('TrainDeleteView/<int:pk>', views.TrainDeleteView.as_view(),name='TrainDeleteView'),

    path('TrainSetListView',views.TrainSetListView.as_view(),name='TrainSetListView'),
    re_path('TrainSetFormView/(?P<parm>\w+)/', views.TrainSetFormView.as_view(), name='TrainSetFormView'),
    path('TrainSetCreateView', views.TrainSetCreateView.as_view(), name='TrainSetCreateView'),
    path('TrainSetUpdateView/<int:pk>', views.TrainSetUpdateView.as_view(), name='TrainSetUpdateView'),
    path('TrainSetDeleteView/<int:pk>', views.TrainSetDeleteView.as_view(),name='TrainSetDeleteView'),



# ]
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)