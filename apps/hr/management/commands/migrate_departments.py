from django.core.management.base import BaseCommand
from apps.hr.models import Employee, Department
from django.db import transaction
import re

class Command(BaseCommand):
    help = 'Migrasi data department dari field dept ke relasi Department'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Jalankan simulasi tanpa menyimpan ke database',
        )

    def generate_unique_code(self, name, existing_codes):
        """Generate unique code dari nama department"""
        # Ambil 3 huruf pertama, uppercase
        base_code = re.sub(r'[^a-zA-Z]', '', name)[:3].upper()
        
        if not base_code:  # Kalau ga ada huruf, pake 'DPT'
            base_code = 'DPT'
        
        code = base_code
        counter = 1
        
        # Loop sampe dapet code yang belum dipake
        while code in existing_codes:
            code = f"{base_code}{counter}"
            counter += 1
        
        return code

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('MIGRASI DATA DEPARTMENT'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        # Hitung total karyawan
        total_karyawan = Employee.objects.count()
        karyawan_dengan_dept = Employee.objects.exclude(dept__isnull=True).exclude(dept='').count()
        
        self.stdout.write(f"Total karyawan: {total_karyawan}")
        self.stdout.write(f"Karyawan dengan dept: {karyawan_dengan_dept}")
        self.stdout.write('')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - TIDAK ADA PERUBAHAN'))
        
        # Koleksi semua department unik dari field dept
        dept_list = Employee.objects.exclude(dept__isnull=True)\
                                    .exclude(dept='')\
                                    .values_list('dept', flat=True)\
                                    .distinct()
        
        # Bersihin nama department
        dept_clean = {}
        for dept in dept_list:
            if dept:
                # Bersihin: hapus spasi berlebih, title case
                clean_name = ' '.join(dept.strip().split())
                clean_name = clean_name.title()
                dept_clean[dept] = clean_name
        
        self.stdout.write(self.style.SUCCESS(f"\nDitemukan {len(dept_clean)} department unik:"))
        
        # Koleksi code yang udah ada di database
        existing_codes = set(Department.objects.values_list('code', flat=True))
        
        # Buat mapping department
        dept_mapping = {}
        for original, clean in dept_clean.items():
            # Generate unique code
            code = self.generate_unique_code(clean, existing_codes)
            
            # Cari atau buat department
            dept, created = Department.objects.get_or_create(
                name=clean,
                defaults={
                    'code': code,
                    'is_active': True
                }
            )
            
            # Tambahkan code ke existing_codes kalo baru dibuat
            if created:
                existing_codes.add(code)
            
            dept_mapping[original] = dept
            
            status = "✓ CREATE" if created else "✓ EXIST"
            self.stdout.write(f"  {status} - '{original}' -> '{clean}' (code: {dept.code})")
        
        self.stdout.write('')
        
        if not dry_run:
            # Update semua employee dengan transaction
            with transaction.atomic():
                updated_count = 0
                skipped_count = 0
                
                for employee in Employee.objects.all():
                    if employee.dept and employee.dept in dept_mapping:
                        employee.department = dept_mapping[employee.dept]
                        employee.save()
                        updated_count += 1
                    else:
                        skipped_count += 1
                
                self.stdout.write(self.style.SUCCESS(f"\nBerhasil mengupdate {updated_count} karyawan"))
                self.stdout.write(f"{skipped_count} karyawan dilewati (tanpa department)")
        else:
            self.stdout.write(self.style.WARNING("\nDry run selesai, tidak ada perubahan di database"))
        
        self.stdout.write(self.style.SUCCESS('=' * 50))