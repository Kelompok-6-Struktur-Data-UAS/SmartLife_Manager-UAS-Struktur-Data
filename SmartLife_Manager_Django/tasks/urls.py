# SmartLife_Manager_Django/tasks/urls.py
from django.urls import path
from . import views

app_name = 'tasks' # Ini mendefinisikan namespace 'tasks'

urlpatterns = [
    path('queue/', views.task_queue_view, name='task_queue'),
    path('add/', views.add_task_view, name='add_task'),
    path('process/', views.process_task_view, name='process_task'),

]