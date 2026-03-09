from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
]
