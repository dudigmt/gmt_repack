from django.core.management.base import BaseCommand
from apps.hr.models import Employee, Position, Department
from django.db import transaction
import re

class Command(BaseCommand):
    help = 'Migrasi data posisi dari field jabatan ke relasi Position'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Jalankan simulasi tanpa menyimpan ke database',
        )

    def generate_unique_code(self, name, existing_codes):
        """Generate unique code dari nama posisi"""
        # Ambil 3 huruf pertama dari kata pertama, uppercase
        words = name.split()
        if words:
            base = words[0][:3].upper()
        else:
            base = 'POS'
        
        # Bersihin dari karakter spesial
        base = re.sub(r'[^A-Z]', '', base)
        
        if not base:  # Kalau ga ada huruf, pake 'POS'
            base = 'POS'
        
        code = base
        counter = 1
        
        # Loop sampe dapet code yang belum dipake
        while code in existing_codes:
            code = f"{base}{counter}"
            counter += 1
        
        return code

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('MIGRASI DATA POSISI'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        # Koleksi semua posisi unik dari field jabatan
        jabatan_list = Employee.objects.exclude(jabatan__isnull=True)\
                                       .exclude(jabatan='')\
                                       .values_list('jabatan', flat=True)\
                                       .distinct()
        
        # Bersihin nama posisi
        jabatan_clean = {}
        for jabatan in jabatan_list:
            if jabatan:
                # Bersihin: hapus spasi berlebih, title case
                clean_name = ' '.join(jabatan.strip().split())
                clean_name = clean_name.title()
                jabatan_clean[jabatan] = clean_name
        
        self.stdout.write(f"Ditemukan {len(jabatan_clean)} posisi unik")
        
        # Koleksi code yang udah ada di database
        existing_codes = set(Position.objects.values_list('code', flat=True))
        
        # Cari atau buat department default untuk posisi yang ga punya department
        default_dept, _ = Department.objects.get_or_create(
            name='Uncategorized',
            defaults={
                'code': 'UNC',
                'is_active': True
            }
        )
        
        # Buat mapping posisi
        posisi_mapping = {}
        for original, clean in jabatan_clean.items():
            # Generate unique code
            code = self.generate_unique_code(clean, existing_codes)
            
            # Cari atau buat posisi
            posisi, created = Position.objects.get_or_create(
                title=clean,
                department=default_dept,  # Sementara pake default
                defaults={
                    'code': code,
                    'is_active': True
                }
            )
            
            # Tambahkan code ke existing_codes kalo baru dibuat
            if created:
                existing_codes.add(code)
            
            posisi_mapping[original] = posisi
            
            status = "✓ CREATE" if created else "✓ EXIST"
            self.stdout.write(f"  {status} - '{original}' -> '{clean}' (code: {posisi.code})")
        
        self.stdout.write('')
        
        if not dry_run:
            with transaction.atomic():
                updated_count = 0
                skipped_count = 0
                
                for employee in Employee.objects.all():
                    if employee.jabatan and employee.jabatan in posisi_mapping:
                        employee.position = posisi_mapping[employee.jabatan]
                        employee.save()
                        updated_count += 1
                    else:
                        skipped_count += 1
                
                self.stdout.write(self.style.SUCCESS(f"\nBerhasil mengupdate {updated_count} karyawan"))
                self.stdout.write(f"{skipped_count} karyawan dilewati (tanpa posisi)")
        else:
            self.stdout.write(self.style.WARNING("\nDry run selesai, tidak ada perubahan di database"))
        
        self.stdout.write(self.style.SUCCESS('=' * 50))