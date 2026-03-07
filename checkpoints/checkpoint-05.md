# GMT Repack - Checkpoint 05

## Status Proyek
- Sidebar telah dihapus, diganti dengan header sticky.
- Halaman utama (dashboard) memerlukan login (`@login_required`).
- Halaman login tidak menampilkan header.
- User profile di pojok kanan header dengan dropdown.
- Container konten terpusat dengan `max-w-7xl mx-auto`.
- Tailwind berfungsi normal.

## Yang Telah Dicapai
- Struktur modular Django dengan folder `apps/`
- Model HR, Production, Warehouse lengkap
- Admin interface untuk semua model
- Dashboard untuk setiap modul (HR, Production, Warehouse) dengan dummy data/agregasi
- Halaman login kustom dengan styling Tailwind
- Autentikasi menggunakan Django built-in auth
- Header sticky dengan user profile (avatar inisial, dropdown)
- Tidak ada sidebar – fokus ke konten utama
- Semua halaman kecuali login memerlukan autentikasi

## Cara Menjalankan
1. Aktifkan virtual environment: `source .venv/bin/activate`
2. Pastikan PostgreSQL berjalan: `sudo service postgresql start` (WSL)
3. Jalankan Tailwind watch (opsional): `npm run watch:css`
4. Jalankan server: `python manage.py runserver`
5. Akses:
   - Root: http://localhost:8000/ (redirect ke login jika belum login)
   - Login: http://localhost:8000/accounts/login/
   - Admin: http://localhost:8000/admin/

## Struktur Direktori
gmt_repack/
├── apps/
│ ├── hr/
│ ├── production/
│ └── warehouse/
├── checkpoints/
├── core/
├── gmt_repack/
├── static/
│ ├── css/
│ │ └── output.css
│ └── src/
│ └── input.css
├── templates/
│ ├── registration/
│ │ └── login.html
│ ├── base.html
│ ├── dashboard.html
│ ├── hr/
│ │ └── dashboard.html
│ ├── production/
│ │ └── dashboard.html
│ └── warehouse/
│ └── dashboard.html
├── .env
├── .env.example
├── .gitignore
├── manage.py
├── package.json
├── postcss.config.js
├── requirements.txt
└── tailwind.config.js


## Catatan
- Untuk menambah modul baru, buat di `apps/` dan daftarkan di `INSTALLED_APPS`.
- Semua dependensi tercatat di `requirements.txt` (Python) dan `package.json` (Node).
- File `.env` berisi konfigurasi rahasia, jangan commit.
- Jika ingin mengubah lebar container, edit class `max-w-7xl` di `base.html` menjadi `max-w-5xl` atau lainnya.
