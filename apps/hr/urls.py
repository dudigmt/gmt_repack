from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/export/', views.export_employees, name='export_employees'),
    path('employees/search/', views.employee_search_api, name='employee_search_api'),
    path('employees/filter-options/', views.get_filter_options, name='get_filter_options'),
]