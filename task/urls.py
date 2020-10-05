from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='sign up'),
    path('login/', views.LoginView.as_view(), name='log in'),
    path('all/', views.all_tasks, name='api all'),
    path('task/<str:slug>', views.api_get_update_delete_task,
         name='api get update delete task'),
    path('new/', views.api_new_task, name='api new'),
    path('task/<str:slug>/changes', views.api_get_task_changes,
         name='api get task changes')
]
