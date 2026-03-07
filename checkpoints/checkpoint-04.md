# GMT Repack - Checkpoint 04

## Status Proyek
Semua modul dasar (HR, Production, Warehouse) telah berfungsi dengan dashboard masing-masing. Semua error telah diperbaiki.

## Yang Telah Dicapai
- Struktur modular Django dengan folder `apps/`
- Model untuk HR (Department, Position, Employee dengan field `role`)
- Model untuk Production (ProductionLine, WorkOrder, WorkOrderAssignment, ProductionLog)
- Model untuk Warehouse (ProductCategory, Product, Warehouse, Stock, StockMovement)
- Admin interface untuk semua model
- Integrasi TailwindCSS dengan npm dan watch mode
- Halaman dashboard utama (home) dengan Tailwind
- Dashboard HR (statistik karyawan, departemen, posisi)
- Dashboard Production (statistik work order, production line, log)
- Dashboard Warehouse (statistik produk, nilai stok, pergerakan stok)
- Semua error terkait query dan template telah diperbaiki
- django-unfold telah diinstal (belum dikonfigurasi)

## Cara Menjalankan
1. Aktifkan virtual environment: `source .venv/bin/activate`
2. Pastikan PostgreSQL berjalan: `sudo service postgresql start` (jika di WSL)
3. Jalankan Tailwind watch (di terminal terpisah): `npm run watch:css`
4. Jalankan Django server: `python manage.py runserver`
5. Akses:
   - Home: http://localhost:8000/
   - HR Dashboard: http://localhost:8000/hr/
   - Production Dashboard: http://localhost:8000/production/
   - Warehouse Dashboard: http://localhost:8000/warehouse/
   - Admin: http://localhost:8000/admin/

## Catatan Penting
- Jika ada data dummy yang ingin ditambahkan, gunakan fixture atau admin.
- Untuk mengaktifkan Unfold, ikuti dokumentasi resmi.
- Semua dependensi tercatat di `requirements.txt` dan `package.json`.
- File `.env` berisi konfigurasi rahasia, jangan commit.

## Struktur Direktori
gmt_repack/
├── apps/
│ ├── hr/
│ │ ├── migrations/
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── tests.py
│ │ ├── urls.py
│ │ └── views.py
│ ├── production/
│ │ ├── migrations/
│ │ ├── init.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── tests.py
│ │ ├── urls.py
│ │ └── views.py
│ └── warehouse/
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── checkpoints/
│ ├── checkpoint-01.md
│ ├── checkpoint-02.md
│ ├── checkpoint-03.md
│ └── checkpoint-04.md
├── core/
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ └── views.py
├── gmt_repack/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── static/
│ ├── css/
│ │ └── output.css
│ └── src/
│ └── input.css
├── templates/
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
├── package-lock.json
├── postcss.config.js
├── requirements.txt
└── tailwind.config.js