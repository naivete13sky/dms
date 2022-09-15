from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile_view',views.profile_view,name='profile_view'),
    path('add_profile',views.add_profile,name='add_profile'),
    re_path('profile/(?P<id>\d+)/$', views.edit_profile,name='edit_profile'),
    path('del_profile/<int:id>/', views.del_profile, name='del_profile'),

    path('ProfileListView',views.ProfileListView.as_view(),name='ProfileListView'),
    re_path('ProfileFormView/(?P<parm>\w+)/', views.ProfileFormView.as_view(), name='ProfileFormView'),
    path('ProfileCreateView', views.ProfileCreateView.as_view(), name='ProfileCreateView'),
    # path('ProfileCreateView/<int:pk>', views.ProfileCreateView.as_view(), name='ProfileCreateView'),
    path('ProfileUpdateView/<int:pk>', views.ProfileUpdateView.as_view(), name='ProfileUpdateView'),
    path('ProfileDeleteView/<int:pk>', views.ProfileDeleteView.as_view(),name='ProfileDeleteView'),

    path('FactoryRuleListView',views.FactoryRuleListView.as_view(),name='FactoryRuleListView'),
    re_path('factoryruleformview/(?P<parm>\w+)/', views.FactoryRuleFormView.as_view(), name='factoryruleformview'),
    path('factoryrule_create', views.FactoryRuleCreateView.as_view(), name='factoryrule_create'),
    path('factoryrule_update/<int:pk>', views.FactoryRuleUpdateView.as_view(), name='factoryrule_update'),
    path('factoryrule_delete/<int:pk>', views.FactoryRuleDeleteView.as_view(),name='factoryrule_delete'),

    path('CustomerRuleListView',views.CustomerRuleListView.as_view(),name='CustomerRuleListView'),
    re_path('CustomerRuleFormView/(?P<parm>\w+)/', views.CustomerRuleFormView.as_view(), name='CustomerRuleFormView'),
    path('CustomerRuleCreateView', views.CustomerRuleCreateView.as_view(), name='CustomerRuleCreateView'),
    path('CustomerRuleUpdateView/<int:pk>', views.CustomerRuleUpdateView.as_view(), name='CustomerRuleUpdateView'),
    path('CustomerRuleDeleteView/<int:pk>', views.CustomerRuleDeleteView.as_view(),name='CustomerRuleDeleteView'),


    path('CustomerListView',views.CustomerListView.as_view(),name='CustomerListView'),
    path('CustomerDetailView/<int:pk>/', views.CustomerDetailView.as_view(),name='CustomerDetailView'),
    path('CustomerUpdateView/<int:pk>', views.CustomerUpdateView.as_view(), name='CustomerUpdateView'),
    path('CustomerCreateView', views.CustomerCreateView.as_view(), name='CustomerCreateView'),
    path('CustomerDeleteView/<int:pk>', views.CustomerDeleteView.as_view(),name='CustomerDeleteView'),

]