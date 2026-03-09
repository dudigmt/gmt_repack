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
    list_display = ['employee_id', 'nama', 'gender', 'department', 'position', 'status_karyawan', 'tgl_rekrut']
    list_filter = ['status_karyawan', 'gender', 'agama', 'gol_darah', 'department', 'position']
    search_fields = ['employee_id', 'nama', 'no_ktp', 'no_hp', 'no_npwp']
    
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