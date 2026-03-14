from django.contrib import admin
from django.contrib import messages
from django.db.models import ProtectedError
from unfold.admin import ModelAdmin
from .models import Department, Position, Employee
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction
from collections import defaultdict
import pandas as pd
from io import BytesIO

@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    
    # CUSTOM ACTIONS
    actions = ['activate_departments', 'deactivate_departments', 'delete_selected_departments', 
               'sync_departments_from_employees']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-departments/', self.admin_site.admin_view(self.sync_departments_view), name='sync-departments'),
            path('sync-full/', self.admin_site.admin_view(self.sync_full_view), name='hr_department_sync_full'),
        ]
        return custom_urls + urls
    
    def sync_full_view(self, request):
        """View untuk sinkronisasi lengkap department + position"""
        # 1. Sync Departments
        dept_values = Employee.objects.exclude(dept__isnull=True).exclude(dept='').values_list('dept', flat=True).distinct()
        
        dept_created = 0
        dept_map = {}
        
        for dept_name in dept_values:
            dept, created = Department.objects.get_or_create(
                name=dept_name,
                defaults={
                    'code': dept_name[:10].upper().replace(' ', '_').replace('|', '_'),
                    'is_active': True
                }
            )
            dept_map[dept_name] = dept
            if created:
                dept_created += 1
        
        # 2. Sync Positions berdasarkan department
        pos_created = 0
        pos_existing = 0
        
        # Kumpulkan semua kombinasi jabatan + department
        data = Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').exclude(dept__isnull=True).exclude(dept='').values_list('jabatan', 'dept').distinct()
        
        for jabatan, dept_name in data:
            if dept_name in dept_map:
                dept = dept_map[dept_name]
                pos, created = Position.objects.get_or_create(
                    title=jabatan,
                    department=dept,
                    defaults={
                        'code': jabatan[:10].upper().replace(' ', '_').replace('|', '_'),
                        'is_active': True
                    }
                )
                if created:
                    pos_created += 1
                else:
                    pos_existing += 1
        
        # 3. Update relasi employee
        emp_updated = 0
        for emp in Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').exclude(dept__isnull=True).exclude(dept=''):
            try:
                pos = Position.objects.get(title=emp.jabatan, department__name=emp.dept)
                if emp.position != pos:
                    emp.position = pos
                    emp.save()
                    emp_updated += 1
            except Position.DoesNotExist:
                pass
        
        self.message_user(
            request,
            f"✅ SINKRONISASI LENGKAP SELESAI!\n"
            f"   📁 Department: {dept_created} baru, {len(dept_map)-dept_created} existing\n"
            f"   📌 Position: {pos_created} baru, {pos_existing} existing\n"
            f"   👥 Employee: {emp_updated} diupdate"
        )
        return redirect('..')
    
    def sync_departments_view(self, request):
        """View untuk sinkronisasi department dari data karyawan"""
        dept_values = Employee.objects.exclude(dept__isnull=True).exclude(dept='').values_list('dept', flat=True).distinct()
        
        created_count = 0
        existing_count = 0
        
        with transaction.atomic():
            for dept_name in dept_values:
                dept, created = Department.objects.get_or_create(
                    name=dept_name,
                    defaults={
                        'code': dept_name[:10].upper().replace(' ', '_').replace('|', '_'),
                        'is_active': True
                    }
                )
                if created:
                    created_count += 1
                else:
                    existing_count += 1
        
        self.message_user(
            request, 
            f"✅ Sinkronisasi department selesai! {created_count} baru, {existing_count} sudah ada"
        )
        return redirect('..')
    
    def sync_departments_from_employees(self, request, queryset):
        """Action untuk sinkronisasi department dari data karyawan"""
        dept_values = Employee.objects.exclude(dept__isnull=True).exclude(dept='').values_list('dept', flat=True).distinct()
        
        created_count = 0
        existing_count = 0
        
        for dept_name in dept_values:
            dept, created = Department.objects.get_or_create(
                name=dept_name,
                defaults={
                    'code': dept_name[:10].upper().replace(' ', '_').replace('|', '_'),
                    'is_active': True
                }
            )
            if created:
                created_count += 1
            else:
                existing_count += 1
        
        self.message_user(
            request, 
            f"✅ Sinkronisasi selesai! {created_count} department baru dibuat, {existing_count} sudah ada"
        )
    sync_departments_from_employees.short_description = "🔄 Sinkronisasi department dari data karyawan"
    
    def activate_departments(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"✅ {count} department berhasil diaktifkan")
    activate_departments.short_description = "Aktifkan department terpilih"
    
    def deactivate_departments(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"✅ {count} department berhasil dinonaktifkan")
    deactivate_departments.short_description = "Nonaktifkan department terpilih"
    
    def delete_selected_departments(self, request, queryset):
        count = queryset.count()
        # Cek apakah ada position yang masih terikat
        protected = []
        for dept in queryset:
            if dept.positions.exists():
                protected.append(dept.name)
        
        if protected:
            self.message_user(
                request, 
                f"❌ Department {', '.join(protected)} masih memiliki posisi, tidak bisa dihapus", 
                level='ERROR'
            )
        else:
            queryset.delete()
            self.message_user(request, f"✅ {count} department berhasil dihapus")
    delete_selected_departments.short_description = "Hapus department terpilih"

@admin.register(Position)
class PositionAdmin(ModelAdmin):
    list_display = ['title', 'code', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['title', 'code']
    
    # CUSTOM ACTIONS
    actions = ['activate_positions', 'deactivate_positions', 'delete_selected_positions',
               'sync_positions_from_employees']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-positions/', self.admin_site.admin_view(self.sync_positions_view), name='sync-positions'),
            path('sync-by-dept/', self.admin_site.admin_view(self.sync_by_dept_view), name='position-sync-by-dept'),
        ]
        return custom_urls + urls
    
    def sync_by_dept_view(self, request):
        """Sinkronisasi position berdasarkan department yang ada"""
        pos_created = 0
        pos_existing = 0
        
        # Kumpulkan semua kombinasi jabatan + department
        data = Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').exclude(dept__isnull=True).exclude(dept='').values_list('jabatan', 'dept').distinct()
        
        for jabatan, dept_name in data:
            try:
                dept = Department.objects.get(name=dept_name)
                pos, created = Position.objects.get_or_create(
                    title=jabatan,
                    department=dept,
                    defaults={
                        'code': jabatan[:10].upper().replace(' ', '_').replace('|', '_'),
                        'is_active': True
                    }
                )
                if created:
                    pos_created += 1
                else:
                    pos_existing += 1
            except Department.DoesNotExist:
                pass
        
        # Update relasi employee
        emp_updated = 0
        for emp in Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').exclude(dept__isnull=True).exclude(dept=''):
            try:
                pos = Position.objects.get(title=emp.jabatan, department__name=emp.dept)
                if emp.position != pos:
                    emp.position = pos
                    emp.save()
                    emp_updated += 1
            except Position.DoesNotExist:
                pass
        
        self.message_user(
            request,
            f"✅ SINKRONISASI POSITION SELESAI!\n"
            f"   📌 Position: {pos_created} baru, {pos_existing} existing\n"
            f"   👥 Employee: {emp_updated} diupdate"
        )
        return redirect('..')
    
    def sync_positions_view(self, request):
        """View untuk sinkronisasi position dari data karyawan (default dept)"""
        pos_values = Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').values_list('jabatan', flat=True).distinct()
        
        default_dept = Department.objects.first()
        if not default_dept:
            self.message_user(request, "❌ Tidak ada department. Jalankan sinkronisasi department dulu!", level='ERROR')
            return redirect('..')
        
        created_count = 0
        existing_count = 0
        
        with transaction.atomic():
            for pos_title in pos_values:
                pos, created = Position.objects.get_or_create(
                    title=pos_title,
                    department=default_dept,
                    defaults={
                        'code': pos_title[:10].upper().replace(' ', '_').replace('|', '_'),
                        'is_active': True
                    }
                )
                if created:
                    created_count += 1
                else:
                    existing_count += 1
        
        self.message_user(
            request, 
            f"✅ Sinkronisasi position selesai! {created_count} baru, {existing_count} sudah ada (semua di {default_dept.name})"
        )
        return redirect('..')
    
    def sync_positions_from_employees(self, request, queryset):
        """Action untuk sinkronisasi position dari data karyawan"""
        pos_values = Employee.objects.exclude(jabatan__isnull=True).exclude(jabatan='').values_list('jabatan', flat=True).distinct()
        
        default_dept = Department.objects.first()
        if not default_dept:
            self.message_user(request, "❌ Tidak ada department. Jalankan sinkronisasi department dulu!", level='ERROR')
            return
        
        created_count = 0
        existing_count = 0
        
        for pos_title in pos_values:
            pos, created = Position.objects.get_or_create(
                title=pos_title,
                department=default_dept,
                defaults={
                    'code': pos_title[:10].upper().replace(' ', '_').replace('|', '_'),
                    'is_active': True
                }
            )
            if created:
                created_count += 1
            else:
                existing_count += 1
        
        self.message_user(
            request, 
            f"✅ Sinkronisasi selesai! {created_count} posisi baru dibuat, {existing_count} sudah ada"
        )
    sync_positions_from_employees.short_description = "🔄 Sinkronisasi posisi dari data karyawan"
    
    def activate_positions(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"✅ {count} posisi berhasil diaktifkan")
    activate_positions.short_description = "Aktifkan posisi terpilih"
    
    def deactivate_positions(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"✅ {count} posisi berhasil dinonaktifkan")
    deactivate_positions.short_description = "Nonaktifkan posisi terpilih"
    
    def delete_selected_positions(self, request, queryset):
        count = queryset.count()
        # Cek apakah ada employee yang masih terikat
        protected = []
        for pos in queryset:
            if pos.employees.exists():
                protected.append(pos.title)
        
        if protected:
            self.message_user(
                request, 
                f"❌ Posisi {', '.join(protected)} masih memiliki karyawan, tidak bisa dihapus", 
                level='ERROR'
            )
        else:
            queryset.delete()
            self.message_user(request, f"✅ {count} posisi berhasil dihapus")
    delete_selected_positions.short_description = "Hapus posisi terpilih"

@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ['employee_id', 'nama', 'gender', 'department', 'position', 'status_karyawan', 'tgl_rekrut']
    list_filter = ['status_karyawan', 'gender', 'agama', 'gol_darah', 'department', 'position']
    search_fields = ['employee_id', 'nama', 'no_ktp', 'no_hp', 'no_npwp']
    
    # CUSTOM ACTIONS UNTUK EMPLOYEE
    actions = [
        'make_tetap', 
        'make_kontrak', 
        'make_os',
        'export_selected_excel',
        'delete_selected_employees',
        'update_department_from_dept',
        'update_position_from_jabatan'
    ]
    
    def update_department_from_dept(self, request, queryset):
        """Update relasi department dari field dept"""
        updated = 0
        not_found = []
        
        for emp in queryset:
            if emp.dept:
                try:
                    dept = Department.objects.get(name=emp.dept)
                    emp.department = dept
                    emp.save()
                    updated += 1
                except Department.DoesNotExist:
                    not_found.append(emp.dept)
        
        msg = f"✅ {updated} karyawan diupdate department-nya"
        if not_found:
            msg += f"\n❌ Department tidak ditemukan: {', '.join(list(set(not_found))[:5])}"
        self.message_user(request, msg)
    update_department_from_dept.short_description = "🔄 Update relasi department dari field 'dept'"
    
    def update_position_from_jabatan(self, request, queryset):
        """Update relasi position dari field jabatan"""
        updated = 0
        not_found = []
        
        for emp in queryset:
            if emp.jabatan:
                try:
                    pos = Position.objects.get(title=emp.jabatan)
                    emp.position = pos
                    emp.save()
                    updated += 1
                except Position.DoesNotExist:
                    not_found.append(emp.jabatan)
        
        msg = f"✅ {updated} karyawan diupdate posisi-nya"
        if not_found:
            msg += f"\n❌ Posisi tidak ditemukan: {', '.join(list(set(not_found))[:5])}"
        self.message_user(request, msg)
    update_position_from_jabatan.short_description = "🔄 Update relasi posisi dari field 'jabatan'"
    
    def make_tetap(self, request, queryset):
        count = queryset.update(status_karyawan='tetap')
        self.message_user(request, f"✅ {count} karyawan diubah status menjadi TETAP")
    make_tetap.short_description = "Ubah status menjadi TETAP"
    
    def make_kontrak(self, request, queryset):
        count = queryset.update(status_karyawan='kontrak')
        self.message_user(request, f"✅ {count} karyawan diubah status menjadi KONTRAK")
    make_kontrak.short_description = "Ubah status menjadi KONTRAK"
    
    def make_os(self, request, queryset):
        count = queryset.update(status_karyawan='os')
        self.message_user(request, f"✅ {count} karyawan diubah status menjadi OS")
    make_os.short_description = "Ubah status menjadi OS"
    
    def export_selected_excel(self, request, queryset):
        # Siapkan data
        data = []
        for emp in queryset:
            data.append({
                'NIK': emp.employee_id,
                'Nama': emp.nama,
                'Status': emp.get_status_karyawan_display(),
                'Department': emp.department.name if emp.department else '-',
                'Posisi': emp.position.title if emp.position else '-',
                'No HP': emp.no_hp,
            })
        
        # Buat dataframe
        df = pd.DataFrame(data)
        
        # Export ke Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Karyawan', index=False)
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="karyawan_export_{request.user.username}.xlsx"'
        
        return response
    export_selected_excel.short_description = "Export ke Excel"
    
    def delete_selected_employees(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"✅ {count} karyawan berhasil dihapus")
    delete_selected_employees.short_description = "Hapus karyawan terpilih"
    
    # Kelompokkan field ke dalam fieldset agar rapi
    fieldsets = (
        ('Data Pribadi', {
            'fields': ('employee_id', 'nama', 'gender', 'tgl_lahir', 'tempat_lahir', 'no_ktp', 'no_kk', 
                      'no_hp', 'alamat', 'kelurahan', 'kecamatan', 'kabupaten_kota', 'kode_pos', 'provinsi',
                      'status_kawin', 'tanggungan', 'agama', 'tinggi_badan', 'berat_badan', 'gol_darah', 'pendidikan')
        }),
        ('Data Kepegawaian', {
            'fields': ('tgl_rekrut', 'status_karyawan', 'tgl_kartetap', 'posisi_karyawan', 'no_kartu_kpk',
                      'group', 'dept', 'jabatan', 'kontrak_ke', 'kontrak_berakhir', 'kode_gaji',
                      'no_rek_bank', 'kode_bank', 'nama_bank')
        }),
        ('BPJS & Pajak', {
            'fields': ('status_ptkp', 'no_npwp', 'status_pajak',
                      'bpjs_tk', 'bpjs_tk_ditanggung', 'bpjs_tk_no',
                      'bpjs_kes', 'bpjs_kes_ditanggung', 'bpjs_kes_no',
                      'faskes', 'placement')
        }),
        ('Data Keluar', {
            'fields': ('tgl_out', 'status_kerja', 'foto')
        }),
        ('Relasi & Metadata', {
            'fields': ('user', 'department', 'position', 'employment_status', 'role', 'hire_date', 
                      'termination_date', 'created_by')
        }),
    )
    
    # Field yang read-only
    readonly_fields = ['created_at', 'updated_at']
    
    # Field untuk pencarian berdasarkan relasi
    raw_id_fields = ['user', 'created_by', 'department', 'position']
    
    # Tanggal hierarki
    date_hierarchy = 'tgl_rekrut'