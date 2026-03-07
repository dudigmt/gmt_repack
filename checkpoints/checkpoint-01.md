# GMT Repack - Project Checkpoint

## Informasi Proyek
- Nama: gmt_repack
- Teknologi: Django 4.2.16, PostgreSQL, TailwindCSS (belum diintegrasikan)
- Environment: Python virtual environment di `.venv`
- Sistem operasi pengembangan: WSL (Ubuntu)

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
│ │ └── views.py
│ ├── production/
│ │ └── (sama seperti di atas)
│ └── warehouse/
│ └── (sama seperti di atas)
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
├── templates/
├── .env
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt

## Aplikasi yang Telah Dibuat
- `core`: Untuk fungsionalitas inti sistem (masih kosong).
- `apps.hr`: Modul Human Resources (model: Department, Position, Employee).
- `apps.production`: Modul Production (model: ProductionLine, WorkOrder, WorkOrderAssignment, ProductionLog).
- `apps.warehouse`: Modul Warehouse (model: ProductCategory, Product, Warehouse, Stock, StockMovement).

## Dependensi (requirements.txt)
- Django==4.2.16
- psycopg2-binary==2.9.9
- python-decouple==3.8

## Konfigurasi Environment (.env)
File `.env` harus berisi variabel berikut:
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=gmt_repack
DB_USER=adung
DB_PASSWORD=1312
DB_HOST=localhost
DB_PORT=5432

Untuk produksi, sesuaikan nilai DEBUG dan SECRET_KEY.

## Database
- PostgreSQL database: `gmt_repack`
- User: `adung` dengan password `1312`
- Migrasi sudah dijalankan (`python manage.py migrate`)

## Superuser
- Username: `adung`
- Password: `1312`
- Email: (kosong)

## Cara Menjalankan
1. Aktifkan virtual environment: `source .venv/bin/activate`
2. Pastikan PostgreSQL berjalan: `sudo service postgresql start`
3. Jalankan server: `python manage.py runserver`
4. Akses admin: http://localhost:8000/admin

## Catatan Penting
- Selalu aktifkan virtual environment sebelum menjalankan perintah Python/Django.
- Jangan commit file `.env` ke version control. Gunakan `.env.example` sebagai template.
- Untuk menambahkan modul baru, buat di dalam folder `apps/` dan daftarkan di `INSTALLED_APPS` dengan prefix `apps.`.
- Jika ada perubahan model, jalankan `python manage.py makemigrations` dan `python manage.py migrate`.
