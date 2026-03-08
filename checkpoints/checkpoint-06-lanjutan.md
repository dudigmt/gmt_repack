# GMT Repack - Checkpoint untuk Chat Baru

## Info Proyek
- Nama: gmt_repack
- Teknologi: Django 4.2.16, PostgreSQL, TailwindCSS
- Path: `/home/adung/projects/gmt_repack`

## Status Terkini
✅ Sidebar dark theme fixed (seperti chat.deepseek.com)
✅ Sidebar di kiri, konten di kanan dengan margin otomatis
✅ Halaman login modern (gradient, card, icon)
✅ Login required untuk semua halaman (kecuali login)
✅ User profile di BOTTOM sidebar (avatar, nama, role, logout)
✅ Unfold terinstal dengan dashboard_callback
✅ Semua error diperbaiki
✅ Push ke GitHub berhasil

## Struktur Penting
- `apps/hr/`, `apps/production/`, `apps/warehouse/` - Modul bisnis
- `core/views.py` - dashboard_callback untuk Unfold
- `templates/base.html` - Base dengan sidebar dark (FIXED), tanpa header
- `templates/registration/login.html` - Login modern
- `static/css/output.css` - CSS hasil build

## Kredensial
- Superuser: adung / 1312
- Database: gmt_repack (user: adung, password: 1312)

## Cara Menjalankan
```bash
cd ~/projects/gmt_repack
source .venv/bin/activate
sudo service postgresql start
npm run watch:css  # opsional
python manage.py runserver

Akses:
http://localhost:8000/ (redirect ke login)
http://localhost:8000/accounts/login/
http://localhost:8000/admin/

Yang Sudah Dicapai
- 3 modul bisnis (HR, Production, Warehouse)
- Dashboard masing-masing modul dengan dummy data
- Sidebar dark theme FIXED (tidak ikut scroll)
- User profile di bagian bawah sidebar
- Halaman login modern dengan validasi
- Autentikasi menggunakan Django auth
- Tailwind terintegrasi penuh
- Unfold siap digunakan

Yang Belum / Bisa Dilanjutkan
-Integrasi Unfold lebih dalam (theming, custom dashboard)
- Role-based access control (field role di Employee)
- Fitur CRUD untuk setiap modul
- Dashboard dengan data real
- Laporan dan export data
- Modul baru (Finance, Purchasing, dll)
- Unit testing

Catatan Penting
- SIDEBAR FIXED, TIDAK ADA HEADER (header dihapus)
- Jangan lupa .env berisi konfigurasi rahasia
- Semua dependensi di requirements.txt dan package.json
- Untuk Unfold: 'unfold' sebelum 'django.contrib.admin' di INSTALLED_APPS