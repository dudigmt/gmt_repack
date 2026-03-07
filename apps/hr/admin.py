from django.contrib import admin
from .models import Department, Position, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['title', 'code']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'position', 'role', 'employment_status', 'hire_date']
    list_filter = ['department', 'position', 'role', 'employment_status', 'gender']
    search_fields = ['employee_id', 'user__username', 'user__first_name', 'user__last_name', 'phone_number']
    raw_id_fields = ['user', 'created_by']
    date_hierarchy = 'hire_date'
