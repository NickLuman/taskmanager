from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='sign up'),
    path('login/', views.LoginView.as_view(), name='log in'),
    path('all/', views.all_tasks, name='api_all'),
    path('task/<str:slug>', views.api_get_update_delete_task, name='api_get_task'),
    path('new/', views.api_new_task, name='api_new'),
    # path('update/<str:slug>', views.api_update_task, name='api_update'),
    # path('delete/<str:slug>', views.api_delete_task, name='api_delete'),
]
