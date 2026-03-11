import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.hr.models import Employee
import os

class Command(BaseCommand):
    help = 'Import employees from Excel file - VERSION ANTI DUP'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        if not os.path.exists(file_path):
            raise CommandError(f'File {file_path} tidak ditemukan')
        
        self.stdout.write(f'Membaca file: {file_path}')
        
        # Hapus semua data lama
        Employee.objects.all().delete()
        self.stdout.write("🗑️  Semua data lama dihapus!")
        
        try:
            # Baca file Excel
            df = pd.read_excel(file_path)
            total = len(df)
            self.stdout.write(f'Ditemukan {total} baris data')
            
            # Cek duplikat NIK dalam file
            df['nik'] = df['nik'].astype(str).str.strip()
            duplicated_nik = df[df.duplicated('nik', keep=False)]
            
            if len(duplicated_nik) > 0:
                self.stdout.write(self.style.WARNING(f"\n⚠️  Ditemukan {len(duplicated_nik)} baris dengan NIK duplikat!"))
                self.stdout.write("Ambil data UNIK saja (keep='first')...")
                
                # Ambil yang pertama saja untuk setiap NIK duplikat
                df = df.drop_duplicates(subset=['nik'], keep='first')
                self.stdout.write(f"   → Menjadi {len(df)} baris unik")
            
            # Import data
            success = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    nik = str(row.get('nik', '')).strip()
                    nama = str(row.get('nama', '')).strip()
                    
                    if not nik or not nama:
                        errors.append(f"Baris {index+2}: NIK/Nama kosong")
                        continue
                    
                    # Buat object
                    emp = Employee(
                        employee_id=nik,
                        nama=nama,
                        gender=None,
                        tgl_lahir=None,
                        tempat_lahir='',
                        no_ktp='',
                        no_kk='',
                        no_hp='',
                        alamat='',
                        kelurahan='',
                        kecamatan='',
                        kabupaten_kota='',
                        kode_pos='',
                        provinsi='',
                        status_kawin=None,
                        tanggungan=0,
                        agama=None,
                        tinggi_badan=None,
                        berat_badan=None,
                        gol_darah=None,
                        pendidikan='',
                        tgl_rekrut=None,
                        status_karyawan='kontrak',
                        tgl_kartetap=None,
                        posisi_karyawan='',
                        no_kartu_kpk='',
                        group='',
                        dept='',
                        jabatan='',
                        kontrak_ke=0,
                        kontrak_berakhir=None,
                        kode_gaji='',
                        no_rek_bank='',
                        kode_bank='',
                        nama_bank='',
                        status_ptkp=None,
                        no_npwp='',
                        bpjs_tk='',
                        bpjs_tk_ditanggung='',
                        bpjs_tk_no='',
                        bpjs_kes='',
                        bpjs_kes_ditanggung='',
                        bpjs_kes_no='',
                        status_pajak=None,
                        faskes='',
                        placement='',
                        tgl_out=None,
                        status_kerja='',
                        foto='',
                        role='operator',
                        employment_status='active'
                    )
                    
                    emp.save()
                    success += 1
                    
                    if success % 100 == 0:
                        self.stdout.write(f"  Progress: {success}/{len(df)}")
                    
                except Exception as e:
                    errors.append(f"Baris {index+2}: {str(e)[:50]}")
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ SUKSES: {success} data"))
            self.stdout.write(self.style.WARNING(f"⚠️  GAGAL: {len(errors)} data"))
            
            if errors:
                self.stdout.write("\nContoh error:")
                for err in errors[:10]:
                    self.stdout.write(f"  {err}")
            
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')