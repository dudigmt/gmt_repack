# GMT Repack - Final Checkpoint Fase 1

## Status Proyek
Proyek dasar dengan tiga modul (HR, Production, Warehouse) telah selesai dibuat dan terintegrasi dengan TailwindCSS.

## Yang Telah Dicapai
- Struktur modular Django dengan folder `apps/`
- Model untuk HR (Department, Position, Employee dengan field `role`)
- Model untuk Production (ProductionLine, WorkOrder, dll)
- Model untuk Warehouse (Product, Stock, StockMovement, dll)
- Admin interface untuk semua model
- Integrasi TailwindCSS dengan npm dan watch mode
- Halaman dashboard sederhana dengan styling Tailwind
- Role-based access control siap (field `role` di Employee)

## Cara Menjalankan
1. Aktifkan virtual environment: `source .venv/bin/activate`
2. Pastikan PostgreSQL berjalan: `sudo service postgresql start` (jika di WSL)
3. Jalankan Tailwind watch (di terminal terpisah): `npm run watch:css`
4. Jalankan Django server: `python manage.py runserver`
5. Akses: http://localhost:8000 (dashboard) dan http://localhost:8000/admin

## Langkah Selanjutnya (Opsional)
- Menambahkan autentikasi/login dengan role-based permissions
- Membuat halaman khusus untuk setiap modul
- Menambahkan laporan dan dashboard interaktif
- Implementasi fitur bisnis spesifik (misal: production scheduling, inventory tracking)
- Integrasi dengan frontend framework jika diperlukan

## Catatan
- Semua dependensi tercatat di `requirements.txt` (Python) dan `package.json` (Node)
- File `.env` menyimpan konfigurasi rahasia, jangan commit
- Struktur siap untuk menambah modul baru di dalam `apps/`
