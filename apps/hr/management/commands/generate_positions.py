from django.core.management.base import BaseCommand
from apps.hr.models import Department, Position, Employee
from django.db import transaction
import re

class Command(BaseCommand):
    help = 'Generate Position berdasarkan Department dan Role'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Jalankan simulasi tanpa menyimpan ke database',
        )

    def generate_code(self, name, existing_codes):
        """Generate unique code dari nama position"""
        # Ambil 3 huruf pertama, uppercase
        base = re.sub(r'[^a-zA-Z]', '', name)[:3].upper()
        if not base:
            base = 'POS'
        
        code = base
        counter = 1
        while code in existing_codes:
            code = f"{base}{counter}"
            counter += 1
        
        return code

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('GENERATE POSITIONS'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

        # Koleksi semua department
        departments = Department.objects.all()
        self.stdout.write(f"Total department: {departments.count()}")

        # Role yang akan dibuat
        roles = [
            ('manager', 'Manager'),
            ('supervisor', 'Supervisor'),
            ('operator', 'Staff'),
        ]

        # Koleksi code yang udah ada
        existing_codes = set(Position.objects.values_list('code', flat=True))
        
        # Hitung rencana pembuatan
        total_planned = departments.count() * len(roles)
        self.stdout.write(f"Rencana pembuatan: {total_planned} positions")
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - TIDAK ADA PERUBAHAN'))

        positions_created = 0
        positions_exist = 0

        # Loop setiap department
        for dept in departments:
            self.stdout.write(f"\nDepartment: {dept.name}")
            
            for role_key, role_name in roles:
                # Nama position: "Manager" atau "Supervisor" atau "Staff"
                title = role_name
                
                # Cek apakah position udah ada
                position, created = Position.objects.get_or_create(
                    title=title,
                    department=dept,
                    defaults={
                        'code': self.generate_code(f"{dept.name[:3]}_{title}", existing_codes),
                        'is_active': True,
                        'description': f"{role_name} di department {dept.name}"
                    }
                )
                
                if created:
                    existing_codes.add(position.code)
                    positions_created += 1
                    status = "✓ CREATE"
                else:
                    positions_exist += 1
                    status = "✓ EXIST"
                
                self.stdout.write(f"  {status} - {title} (code: {position.code})")

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(f"Total positions: {positions_created + positions_exist}")
        self.stdout.write(f"  - Created: {positions_created}")
        self.stdout.write(f"  - Already exist: {positions_exist}")

        if not dry_run and positions_created > 0:
            self.stdout.write(self.style.SUCCESS('\n✅ Positions berhasil digenerate!'))
        elif dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  Dry run selesai, tidak ada perubahan'))