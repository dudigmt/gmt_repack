# GMT Repack - Checkpoint setelah Instalasi Unfold

## Status Proyek
Proyek dasar dengan tiga modul (HR, Production, Warehouse) telah selesai dibuat, terintegrasi dengan TailwindCSS, dan django-unfold telah diinstal (namun belum dikonfigurasi).

## Yang Telah Dicapai
- Struktur modular Django dengan folder `apps/`
- Model untuk HR (Department, Position, Employee dengan field `role`)
- Model untuk Production (ProductionLine, WorkOrder, dll)
- Model untuk Warehouse (Product, Stock, StockMovement, dll)
- Admin interface untuk semua model
- Integrasi TailwindCSS dengan npm dan watch mode
- Halaman dashboard sederhana dengan styling Tailwind
- Role-based access control siap (field `role` di Employee)
- django-unfold telah diinstal (versi terbaru) dan tercatat di requirements.txt

## Cara Menjalankan
1. Aktifkan virtual environment: `source .venv/bin/activate`
2. Pastikan PostgreSQL berjalan: `sudo service postgresql start` (jika di WSL)
3. Jalankan Tailwind watch (di terminal terpisah): `npm run watch:css`
4. Jalankan Django server: `python manage.py runserver`
5. Akses: http://localhost:8000 (dashboard) dan http://localhost:8000/admin

## Langkah Selanjutnya (untuk mengaktifkan Unfold)
1. Ikuti petunjuk instalasi di https://django-unfold.readthedocs.io/en/latest/installation.html
2. Secara umum: tambahkan 'unfold' dan 'unfold.contrib.filters' ke INSTALLED_APPS sebelum 'django.contrib.admin'
3. Sesuaikan template dan konfigurasi lainnya sesuai kebutuhan

## Catatan
- Semua dependensi tercatat di `requirements.txt` (Python) dan `package.json` (Node)
- File `.env` menyimpan konfigurasi rahasia, jangan commit
- Struktur siap untuk menambah modul baru di dalam `apps/`
