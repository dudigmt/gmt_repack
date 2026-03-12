import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.hr.models import Employee
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Import employees from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel file')
        parser.add_argument('--dry-run', action='store_true', help='Simulate import without saving to database')

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
        mapping = {
            'TK0': 'tk0', 'TK/0': 'tk0', 'TK-0': 'tk0', 'TK 0': 'tk0',
            'TK1': 'tk1', 'TK/1': 'tk1', 'TK-1': 'tk1', 'TK 1': 'tk1',
            'TK2': 'tk2', 'TK/2': 'tk2', 'TK-2': 'tk2', 'TK 2': 'tk2',
            'TK3': 'tk3', 'TK/3': 'tk3', 'TK-3': 'tk3', 'TK 3': 'tk3',
            'K0': 'k0', 'K/0': 'k0', 'K-0': 'k0', 'K 0': 'k0',
            'K1': 'k1', 'K/1': 'k1', 'K-1': 'k1', 'K 1': 'k1',
            'K2': 'k2', 'K/2': 'k2', 'K-2': 'k2', 'K 2': 'k2',
            'K3': 'k3', 'K/3': 'k3', 'K-3': 'k3', 'K 3': 'k3',
        }
        return mapping.get(val, None)

    def normalize_status_pajak(self, value):
        if pd.isna(value) or not value:
            return 'non_npwp'
        val = str(value).lower().strip()
        if 'npwp' in val or 'ya' in val or 'yes' in val or 'ada' in val:
            return 'npwp'
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

    def normalize_status_karyawan(self, value):
        if pd.isna(value) or not value:
            return 'kontrak'
        val = str(value).lower().strip()
        if 'tetap' in val:
            return 'tetap'
        elif 'kontrak' in val or 'contract' in val:
            return 'kontrak'
        elif 'os' in val or 'outsourcing' in val or 'out source' in val:
            return 'os'
        return 'kontrak'

    def normalize_employment_status(self, status_karyawan):
        mapping = {
            'tetap': 'active',
            'kontrak': 'active',
            'os': 'active',
        }
        return mapping.get(status_karyawan, 'active')

    def parse_date(self, value):
        if pd.isna(value) or not value:
            return None
        if isinstance(value, (pd.Timestamp, datetime)):
            return value.date() if hasattr(value, 'date') else value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        return None

    def parse_int(self, value):
        if pd.isna(value) or not value:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def parse_float(self, value):
        if pd.isna(value) or not value:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def clean_text(self, value):
        if pd.isna(value) or not value:
            return ''
        return str(value).strip()

    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options.get('dry_run', False)
        
        if not os.path.exists(file_path):
            raise CommandError(f'File {file_path} tidak ditemukan')
        
        self.stdout.write(f'\n📁 Membaca file: {file_path}')
        
        try:
            # Baca file Excel
            df = pd.read_excel(file_path)
            total_rows = len(df)
            self.stdout.write(f'📊 Total data di Excel: {total_rows}\n')
            
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
            
            # Ganti nama kolom yang ada
            available_columns = [col for col in column_mapping.keys() if col in df.columns]
            rename_dict = {col: column_mapping[col] for col in available_columns}
            df.rename(columns=rename_dict, inplace=True)
            
            # Bersihkan data
            df = df.replace([np.nan, pd.NA, pd.NaT, 'nan', 'NaN', 'NAN', 'None', 'none', ''], None)
            
            success_count = 0
            error_count = 0
            error_details = []
            
            # Kumpulkan NIK yang sudah ada di database
            existing_niks = set(Employee.objects.values_list('employee_id', flat=True))
            
            for index, row in df.iterrows():
                sid = transaction.savepoint()
                try:
                    # Ambil NIK
                    employee_id = row.get('employee_id')
                    if pd.isna(employee_id) or not employee_id:
                        error_msg = f"Baris {index+2}: NIK kosong"
                        self.stdout.write(self.style.ERROR(f'  ❌ {error_msg}'))
                        error_count += 1
                        error_details.append(error_msg)
                        transaction.savepoint_rollback(sid)
                        continue
                    
                    employee_id = str(employee_id).strip()
                    original_nik = employee_id
                    
                    # CEK DUPLIKAT NIK - LANGSUNG TOLAK
                    if employee_id in existing_niks:
                        error_msg = f"Baris {index+2}: {employee_id} - {row.get('nama', '')} - ERROR: NIK sudah ada di database"
                        self.stdout.write(self.style.ERROR(f'  ❌ {error_msg}'))
                        error_count += 1
                        error_details.append(error_msg)
                        transaction.savepoint_rollback(sid)
                        continue
                    
                    if employee_id != original_nik:
                        # Ini duplikat, tapi tetap kita lanjut
                        pass
                    
                    # Siapkan data
                    data = {}
                    for col in df.columns:
                        val = row.get(col)
                        if val is not None:
                            data[col] = val
                    
                    # Normalisasi field-field
                    text_fields = ['nama', 'tempat_lahir', 'alamat', 'kelurahan', 'kecamatan', 
                                  'kabupaten_kota', 'provinsi', 'pendidikan', 'posisi_karyawan',
                                  'group', 'dept', 'jabatan', 'kode_gaji', 'no_rek_bank',
                                  'kode_bank', 'nama_bank', 'no_npwp', 'bpjs_tk', 'bpjs_kes',
                                  'faskes', 'placement', 'status_kerja', 'foto']
                    
                    for field in text_fields:
                        if field in data:
                            data[field] = self.clean_text(data[field])
                    
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
                    
                    if 'status_karyawan' in data:
                        data['status_karyawan'] = self.normalize_status_karyawan(data['status_karyawan'])
                        data['employment_status'] = self.normalize_employment_status(data['status_karyawan'])
                    
                    # Tanggal
                    date_fields = ['tgl_lahir', 'tgl_rekrut', 'tgl_kartetap', 'kontrak_berakhir', 'tgl_out']
                    for field in date_fields:
                        if field in data:
                            data[field] = self.parse_date(data[field])
                    
                    # Numeric
                    if 'tanggungan' in data:
                        data['tanggungan'] = self.parse_int(data['tanggungan']) or 0
                    
                    if 'kontrak_ke' in data:
                        data['kontrak_ke'] = self.parse_int(data['kontrak_ke']) or 0
                    
                    if 'tinggi_badan' in data:
                        data['tinggi_badan'] = self.parse_float(data['tinggi_badan'])
                    
                    if 'berat_badan' in data:
                        data['berat_badan'] = self.parse_float(data['berat_badan'])
                    
                    # Simpan
                    if dry_run:
                        # Dry run - no save
                        transaction.savepoint_rollback(sid)
                    else:
                        data['employee_id'] = employee_id
                        Employee.objects.create(**data)
                        transaction.savepoint_commit(sid)
                        existing_niks.add(employee_id)  # Tambah ke set
                    
                    success_count += 1
                    
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    nama = row.get('nama', '')
                    if pd.isna(nama):
                        nama = ''
                    error_msg = f"Baris {index+2}: {original_nik} - {str(nama)[:30]} - ERROR: {str(e)}"
                    self.stdout.write(self.style.ERROR(f'  ❌ {error_msg}'))
                    error_count += 1
                    error_details.append(error_msg)
            
            # ========== SUMMARY ==========
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('📊 RINGKASAN IMPORT:'))
            # self.stdout.write('='*60)
            self.stdout.write(f'📁 Total data di Excel    : {total_rows}')
            self.stdout.write(f'✅ Berhasil diimport     : {success_count}')
            self.stdout.write(f'❌ Gagal                 : {error_count}')
            # self.stdout.write('='*60)
            
            if error_details:
                self.stdout.write(self.style.ERROR('\n🔥 DATA GAGAL IMPORT:'))
                for i, err in enumerate(error_details, 1):
                    self.stdout.write(f'   {i}. {err}')
                self.stdout.write('='*60)
            
            if dry_run:
                self.stdout.write(self.style.WARNING('\n⚠️  DRY RUN MODE - Tidak ada data yang tersimpan'))
                self.stdout.write('='*60)
            
        except Exception as e:
            raise CommandError(f'Error membaca file: {str(e)}')