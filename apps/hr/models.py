from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='positions')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'department']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.title} ({self.department.name})"

class Employee(models.Model):
    EMPLOYMENT_STATUS = (
        ('active', 'Active'),
        ('probation', 'Probation'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
    )

    GENDER = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),        
    )

    AGAMA = (
        ('islam', 'Islam'),
        ('kristen', 'Kristen'),
        ('katolik', 'Katolik'),
        ('hindu', 'Hindu'),
        ('buddha', 'Buddha'),
        ('konghucu', 'Konghucu'),
    )

    GOL_DARAH = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    )

    STATUS_KAWIN = (
        ('bk', 'Belum Kawin'),
        ('kawin', 'Kawin'),
        ('cerai', 'Cerai'),
        ('cerai_mati', 'Cerai Mati'),
    )

    STATUS_KARYAWAN = (
        ('tetap', 'Tetap'),
        ('kontrak', 'Kontrak'),
        ('os', 'OS'),
        ('probation', 'Probation'),
        ('harian', 'Harian'),
    )

    STATUS_PTK = (
        ('tk0', 'TK0'),
        ('tk1', 'TK1'),
        ('tk2', 'TK2'),
        ('tk3', 'TK3'),
        ('k0', 'K0'),
        ('k1', 'K1'),
        ('k2', 'K2'),
        ('k3', 'K3'),
    )

    STATUS_PAJAK = (
        ('npwp', 'Memiliki NPWP'),
        ('non_npwp', 'Tidak Memiliki NPWP'),
    )


    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('hr', 'HR Staff'),
        ('production', 'Production Staff'),
        ('warehouse', 'Warehouse Staff'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')

    # Relasi ke User (tetap)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    
    # Data Pribadi
    employee_id = models.CharField(max_length=20, unique=True, help_text="NIK Karyawan")
    nama = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    tgl_lahir = models.DateField(null=True, blank=True)
    tempat_lahir = models.CharField(max_length=100, blank=True)
    no_ktp = models.CharField(max_length=30, unique=True, blank=True, null=True)
    no_kk = models.CharField(max_length=30, blank=True)
    no_hp = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    kelurahan = models.CharField(max_length=100, blank=True)
    kecamatan = models.CharField(max_length=100, blank=True)
    kabupaten_kota = models.CharField(max_length=100, blank=True)
    kode_pos = models.CharField(max_length=10, blank=True)
    provinsi = models.CharField(max_length=100, blank=True)
    status_kawin = models.CharField(max_length=20, choices=STATUS_KAWIN, blank=True, null=True)
    tanggungan = models.IntegerField(default=0, blank=True, null=True)
    agama = models.CharField(max_length=20, choices=AGAMA, blank=True, null=True)
    tinggi_badan = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    berat_badan = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gol_darah = models.CharField(max_length=2, choices=GOL_DARAH, blank=True, null=True)
    pendidikan = models.CharField(max_length=50, blank=True)

    # Data Kepegawaian
    tgl_rekrut = models.DateField(null=True, blank=True)
    status_karyawan = models.CharField(max_length=20, choices=STATUS_KARYAWAN, default='kontrak')
    tgl_kartetap = models.DateField(null=True, blank=True)
    posisi_karyawan = models.CharField(max_length=100, blank=True)
    no_kartu_kpk = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=100, blank=True)
    dept = models.CharField(max_length=100, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)
    kontrak_ke = models.IntegerField(default=0, blank=True, null=True)
    kontrak_berakhir = models.DateField(null=True, blank=True)
    kode_gaji = models.CharField(max_length=20, blank=True)
    no_rek_bank = models.CharField(max_length=50, blank=True)
    kode_bank = models.CharField(max_length=10, blank=True)
    nama_bank = models.CharField(max_length=50, blank=True)

    # Data BPJS & Pajak
    status_ptkp = models.CharField(max_length=10, choices=STATUS_PTK, blank=True, null=True)
    no_npwp = models.CharField(max_length=30, blank=True)
    bpjs_tk = models.CharField(max_length=50, blank=True)
    bpjs_tk_ditanggung = models.CharField(max_length=100, blank=True)
    bpjs_tk_no = models.CharField(max_length=30, blank=True)
    bpjs_kes = models.CharField(max_length=50, blank=True)
    bpjs_kes_ditanggung = models.CharField(max_length=100, blank=True)
    bpjs_kes_no = models.CharField(max_length=30, blank=True)
    status_pajak = models.CharField(max_length=20, choices=STATUS_PAJAK, blank=True, null=True)
    faskes = models.CharField(max_length=100, blank=True)
    placement = models.CharField(max_length=100, blank=True)

    # Data Keluar
    tgl_out = models.DateField(null=True, blank=True)
    status_kerja = models.CharField(max_length=20, blank=True)
    foto = models.CharField(max_length=255, blank=True)

    # Metadata
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='employees', null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    hire_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_employees')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_employees')

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.employee_id} - {self.nama or self.user.get_full_name() if self.user else 'No User'}"
