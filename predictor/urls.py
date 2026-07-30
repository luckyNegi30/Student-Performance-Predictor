from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-history/', views.delete_history, name='delete_history'),
    path('view/<int:id>/', views.view_prediction, name='view_prediction'),
    path('delete/<int:id>/', views.delete_prediction, name='delete_prediction'),
path('view-result/<int:id>/', views.view_result_ajax, name='view_result_ajax'),
]

