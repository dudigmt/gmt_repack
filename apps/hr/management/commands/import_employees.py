import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.hr.models import Employee
import os

class Command(BaseCommand):
    help = 'Import employees from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        if not os.path.exists(file_path):
            raise CommandError(f'File {file_path} tidak ditemukan')
        
        self.stdout.write(f'Membaca file: {file_path}')
        
        try:
            # Baca file Excel
            df = pd.read_excel(file_path)
            self.stdout.write(f'Ditemukan {len(df)} baris data')
            
            # Mapping kolom Excel ke field model
            column_mapping = {
                'nik': 'employee_id',
                'nama': 'nama',
                'sex': 'gender',
                'tgl_lahir': 'tgl_lahir',
                'tempat_lahir': 'tempat_lahir',
                'no_ktp': 'no_ktp',
                'no_kk': 'no_kk',
                'no_hp': 'no_hp',
                'alamat': 'alamat',
                'kelurahan': 'kelurahan',
                'kecamatan': 'kecamatan',
                'kabupaten_kota': 'kabupaten_kota',
                'kode_pos': 'kode_pos',
                'provinsi': 'provinsi',
                'status_kawin': 'status_kawin',
                'tanggungan': 'tanggungan',
                'agama': 'agama',
                'tinggi_badan': 'tinggi_badan',
                'berat_badan': 'berat_badan',
                'gol_darah': 'gol_darah',
                'pendidikan': 'pendidikan',
                'tgl_rekrut': 'tgl_rekrut',
                'status_karyawan': 'status_karyawan',
                'tgl_kartetap': 'tgl_kartetap',
                'posisi_karyawan': 'posisi_karyawan',
                'no_kartu_kpk': 'no_kartu_kpk',
                'group': 'group',
                'dept': 'dept',
                'jabatan': 'jabatan',
                'kontrak_ke': 'kontrak_ke',
                'kontrak_berakhir': 'kontrak_berakhir',
                'kode_gaji': 'kode_gaji',
                'no_rek_bank': 'no_rek_bank',
                'kode_bank': 'kode_bank',
                'nama_bank': 'nama_bank',
                'status_ptkp': 'status_ptkp',
                'no_npwp': 'no_npwp',
                'bpjs_tk': 'bpjs_tk',
                'bpjs_tk_ditanggung': 'bpjs_tk_ditanggung',
                'bpjs_tk_no': 'bpjs_tk_no',
                'bpjs_kes': 'bpjs_kes',
                'bpjs_kes_ditanggung': 'bpjs_kes_ditanggung',
                'bpjs_kes_no': 'bpjs_kes_no',
                'status_pajak': 'status_pajak',
                'faskes': 'faskes',
                'placement': 'placement',
                'tgl_out': 'tgl_out',
                'status_kerja': 'status_kerja',
                'foto': 'foto'
            }
            
            # Ganti nama kolom sesuai mapping
            df.rename(columns=column_mapping, inplace=True)
            
            # Bersihkan data: ganti semua nilai kosong (NaN, 'nan', '') dengan None
            df = df.replace([np.nan, pd.NA, pd.NaT, 'nan', 'NaN', 'NAN', ''], None)
            
            success_count = 0
            error_count = 0
            error_details = []
            
            # Import dengan savepoint per baris
            for index, row in df.iterrows():
                # Buat savepoint
                sid = transaction.savepoint()
                try:
                    # Cek apakah employee sudah ada berdasarkan employee_id
                    employee_id = row.get('employee_id')
                    if not employee_id:
                        self.stdout.write(self.style.WARNING(f'Baris {index+2}: NIK kosong, dilewati'))
                        error_count += 1
                        error_details.append(f'Baris {index+2}: NIK kosong')
                        transaction.savepoint_rollback(sid)
                        continue
                    
                    # Konversi row ke dictionary, buang kolom yang None
                    data = {k: v for k, v in row.items() if v is not None}
                    
                    # Update atau create
                    obj, created = Employee.objects.update_or_create(
                        employee_id=employee_id,
                        defaults=data
                    )
                    
                    # Commit savepoint
                    transaction.savepoint_commit(sid)
                    
                    if created:
                        self.stdout.write(f'  + Baris {index+2}: {employee_id} - {row.get("nama", "")} (created)')
                    else:
                        self.stdout.write(f'  ~ Baris {index+2}: {employee_id} - {row.get("nama", "")} (updated)')
                    
                    success_count += 1
                    
                except Exception as e:
                    # Rollback savepoint
                    transaction.savepoint_rollback(sid)
                    self.stdout.write(self.style.ERROR(f'  X Baris {index+2}: Error - {str(e)}'))
                    error_count += 1
                    error_details.append(f'Baris {index+2}: {str(e)}')
                
            self.stdout.write(self.style.SUCCESS(f'\nSelesai! {success_count} berhasil, {error_count} gagal'))
            if error_details:
                self.stdout.write(self.style.WARNING('Detail error:'))
                for err in error_details:
                    self.stdout.write(f'  {err}')
            
        except Exception as e:
            raise CommandError(f'Error membaca file: {str(e)}')