from django.shortcuts import render
from .models import Employee, Department, Position
from django.db.models import Count

def dashboard(request):
    # Dummy data / agregasi dari database
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_positions = Position.objects.count()
    
    # Data untuk chart/statistik sederhana
    employees_by_dept = Department.objects.annotate(emp_count=Count('employees')).values('name', 'emp_count')
    employees_by_status = Employee.objects.values('employment_status').annotate(count=Count('id'))
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_positions': total_positions,
        'employees_by_dept': employees_by_dept,
        'employees_by_status': employees_by_status,
    }
    return render(request, 'hr/dashboard.html', context)