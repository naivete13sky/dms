from django.urls import path,re_path
from restful_api import views
app_name = 'restful_api'

urlpatterns = [
    re_path(r'^api/tutorials$', views.tutorial_list),
    re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    re_path(r'^api/tutorials/published$', views.tutorial_list_published)
]