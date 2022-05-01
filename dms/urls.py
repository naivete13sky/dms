"""dms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from job_manage import views


from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from job_manage.sitemaps import JobSitemap
sitemaps = {'jobs': JobSitemap,}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('job_manage/', include('job_manage.urls', namespace='job_manage')),
    path('back_stage/', include('back_stage.urls', namespace='back_stage')),
    path('router_job_odb/<order>', views.file_download_odb, name='file_download_odb'),
    path('media/files/<order>', views.file_download, name='file_download'),


    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('job_manage.urls', namespace='job_index')),
    path('project/', include('project.urls', namespace='project')),
    path('order/', include('order.urls', namespace='order')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)