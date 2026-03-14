gmt_repack/
├── static/
│   ├── css/
│   │   ├── base/
│   │   │   ├── variables.css      # Warna, font, spacing, dll
│   │   │   ├── reset.css          # Reset CSS dasar
│   │   │   ├── typography.css     # Styling teks
│   │   │   ├── layout.css         # Sidebar, main container
│   │   │   └── utilities.css      # Helper classes
│   │   ├── components/
│   │   │   ├── buttons.css        # Semua tombol
│   │   │   ├── cards.css          # Stat cards, employee cards
│   │   │   ├── tables.css         # Tabel karyawan
│   │   │   ├── forms.css          # Input, search, select
│   │   │   ├── modals.css         # Filter modal
│   │   │   ├── badges.css         # Status badges
│   │   │   ├── avatars.css        # Avatar inisial
│   │   │   └── dropdowns.css      # Export, column visibility
│   │   ├── pages/
│   │   │   └── hr/
│   │   │       └── employee-list.css  # Halaman spesifik
│   │   └── main.css               # Import semua file di atas
│   └── js/
│       ├── components/
│       │   ├── hover-card.js      # Hover card preview
│       │   ├── search-debounce.js # Search dengan debounce
│       │   ├── filter-chips.js    # Filter chips
│       │   └── modals.js          # Modal handler
│       └── pages/
│           └── hr/
│               └── employee-list.js  # JS untuk halaman karyawan
├── templates/
│   ├── base.html                   # MODIF - hapus semua inline style
│   └── hr/
│       └── employee_list.html      # MODIF - panggil JS/CSS terpisah
├── tailwind.config.js              # MODIF - update content paths
└── gmt_repack/
    └── settings.py                  # CEK - static files config


    