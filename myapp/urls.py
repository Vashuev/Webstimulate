from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.user_dashboard, name='user_dashboard'),
    path('user_dashboard/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
    path('entry/update_remarks/<int:entry_id>/', views.update_user_remarks, name='update_user_remarks'),
    path('entry/update_status/<int:entry_id>/', views.update_user_status, name='update_user_status'),
    path('entry/update/<int:pk>/', views.update_entry, name='update_entry'),
    path('status_meanings/', views.status_meanings, name='status_meanings'),
    path('admin_dashboard/bulk-upload/', views.bulk_upload_view, name='bulk_upload_view'),
    path('admin_dashboard/download-example-csv/', views.download_example_csv, name='download_example_csv'),
]