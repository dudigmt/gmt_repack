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

    def normalize_status_kawin(self, value):
        if pd.isna(value) or not value:
            return None
        val = str(value).lower().strip()
        if 'belum' in val or 'bk' in val:
            return 'bk'
        elif 'kawin' in val:
            return 'kawin'
        elif 'cerai' in val:
            return 'cerai'
        elif 'cerai mati' in val or 'cerai_mati' in val:
            return 'cerai_mati'
        return None

    def normalize_agama(self, value):
        if pd.isna(value) or not value:
            return None
        val = str(value).lower().strip()
        if 'islam' in val:
            return 'islam'
        elif 'kristen' in val:
            return 'kristen'
        elif 'katolik' in val:
            return 'katolik'
        elif 'hindu' in val:
            return 'hindu'
        elif 'buddha' in val or 'budha' in val:
            return 'buddha'
        elif 'konghucu' in val:
            return 'konghucu'
        return None

    def normalize_status_ptkp(self, value):
        if pd.isna(value) or not value:
            return None
        val = str(value).upper().strip().replace('/', '').replace('-', '').replace(' ', '')
        # Mapping umum
        mapping = {
            'TK0': 'tk0', 'TK/0': 'tk0', 'TK-0': 'tk0',
            'TK1': 'tk1', 'TK/1': 'tk1', 'TK-1': 'tk1',
            'TK2': 'tk2', 'TK/2': 'tk2', 'TK-2': 'tk2',
            'TK3': 'tk3', 'TK/3': 'tk3', 'TK-3': 'tk3',
            'K0': 'k0', 'K/0': 'k0', 'K-0': 'k0',
            'K1': 'k1', 'K/1': 'k1', 'K-1': 'k1',
            'K2': 'k2', 'K/2': 'k2', 'K-2': 'k2',
            'K3': 'k3', 'K/3': 'k3', 'K-3': 'k3',
        }
        return mapping.get(val, None)

    def normalize_status_pajak(self, value):
        if pd.isna(value) or not value:
            return None
        val = str(value).lower().strip()
        if 'npwp' in val:
            return 'npwp'
        else:
            return 'non_npwp'

    def normalize_gender(self, value):
        if pd.isna(value) or not value:
            return None
        val = str(value).upper().strip()
        if val in ['L', 'LAKI', 'LAKI-LAKI', 'LAKILAKI', 'MALE', 'M']:
            return 'L'
        elif val in ['P', 'PEREMPUAN', 'WANITA', 'FEMALE', 'F']:
            return 'P'
        return None

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
            
            # Bersihkan data: ganti semua nilai kosong dengan None
            df = df.replace([np.nan, pd.NA, pd.NaT, 'nan', 'NaN', 'NAN', ''], None)
            
            success_count = 0
            error_count = 0
            error_details = []
            
            # Import dengan savepoint per baris
            for index, row in df.iterrows():
                sid = transaction.savepoint()
                try:
                    employee_id = row.get('employee_id')
                    if not employee_id:
                        self.stdout.write(self.style.WARNING(f'Baris {index+2}: NIK kosong, dilewati'))
                        error_count += 1
                        error_details.append(f'Baris {index+2}: NIK kosong')
                        transaction.savepoint_rollback(sid)
                        continue
                    
                    # Konversi row ke dictionary
                    data = {k: v for k, v in row.items() if v is not None}
                    
                    # Normalisasi field-field penting
                    if 'gender' in data:
                        data['gender'] = self.normalize_gender(data['gender'])
                    
                    if 'status_kawin' in data:
                        data['status_kawin'] = self.normalize_status_kawin(data['status_kawin'])
                    
                    if 'agama' in data:
                        data['agama'] = self.normalize_agama(data['agama'])
                    
                    if 'status_ptkp' in data:
                        data['status_ptkp'] = self.normalize_status_ptkp(data['status_ptkp'])
                    
                    if 'status_pajak' in data:
                        data['status_pajak'] = self.normalize_status_pajak(data['status_pajak'])
                    
                    # Update atau create
                    obj, created = Employee.objects.update_or_create(
                        employee_id=employee_id,
                        defaults=data
                    )
                    
                    transaction.savepoint_commit(sid)
                    
                    if created:
                        self.stdout.write(f'  + Baris {index+2}: {employee_id} - {data.get("nama", "")} (created)')
                    else:
                        self.stdout.write(f'  ~ Baris {index+2}: {employee_id} - {data.get("nama", "")} (updated)')
                    
                    success_count += 1
                    
                except Exception as e:
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