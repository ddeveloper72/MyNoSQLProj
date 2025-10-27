from django.urls import path
from . import views

app_name = 'djangonosql'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/users/', views.UserListView.as_view(), name='user_list'),
    path('api/tasks/', views.TaskListView.as_view(), name='task_list'),
    path('api/analytics/', views.ProjectAnalyticsView.as_view(), name='analytics'),
    path('api/test-connection/', views.mongodb_connection_test, name='test_connection'),
]