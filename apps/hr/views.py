from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
from django.core.management import call_command
from django.conf import settings
import os
import tempfile

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

@staff_member_required
def import_employees_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Simpan file sementara
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
        
        try:
            # Panggil management command
            from io import StringIO
            output = StringIO()
            call_command('import_employees', tmp_path, stdout=output)
            
            # Tampilkan output ke user
            messages.success(request, f'Import berhasil!\n\n{output.getvalue()}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        finally:
            # Hapus file sementara
            os.unlink(tmp_path)
        
        return redirect('admin:hr_employee_changelist')
    
    return redirect('admin:hr_employee_changelist')