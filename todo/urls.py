from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.todo_list, name='list'),
    path('', views.home, name='home')
]
