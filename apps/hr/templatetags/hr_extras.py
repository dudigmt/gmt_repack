from django import template
import random

register = template.Library()

@register.filter
def avatar_color(department):
    """
    Mengembalikan kelas warna Tailwind berdasarkan department dengan variasi gradient.
    Jika department tidak ada, kembalikan warna default abu-abu.
    """
    # Gradient colors yang cantik untuk avatar
    gradients = [
        'bg-gradient-to-br from-blue-500 to-indigo-600',
        'bg-gradient-to-br from-green-500 to-emerald-600',
        'bg-gradient-to-br from-yellow-500 to-orange-600',
        'bg-gradient-to-br from-red-500 to-pink-600',
        'bg-gradient-to-br from-purple-500 to-violet-600',
        'bg-gradient-to-br from-pink-500 to-rose-600',
        'bg-gradient-to-br from-teal-500 to-cyan-600',
        'bg-gradient-to-br from-indigo-500 to-purple-600',
        'bg-gradient-to-br from-orange-500 to-red-600',
        'bg-gradient-to-br from-cyan-500 to-blue-600',
        'bg-gradient-to-br from-lime-500 to-green-600',
        'bg-gradient-to-br from-emerald-500 to-teal-600',
        'bg-gradient-to-br from-violet-500 to-purple-600',
        'bg-gradient-to-br from-fuchsia-500 to-pink-600',
        'bg-gradient-to-br from-rose-500 to-red-600',
        'bg-gradient-to-br from-amber-500 to-yellow-600',
    ]
    
    if department and department.name:
        # Gunakan hash dari nama department untuk konsistensi
        index = hash(department.name) % len(gradients)
        return gradients[index]
    
    # Default gradient untuk user tanpa department
    return 'bg-gradient-to-br from-gray-500 to-gray-600'

@register.filter
def avatar_color_static(department_name):
    """
    Versi alternatif yang menerima string nama department langsung
    """
    gradients = [
        'bg-gradient-to-br from-blue-500 to-indigo-600',
        'bg-gradient-to-br from-green-500 to-emerald-600',
        'bg-gradient-to-br from-yellow-500 to-orange-600',
        'bg-gradient-to-br from-red-500 to-pink-600',
        'bg-gradient-to-br from-purple-500 to-violet-600',
        'bg-gradient-to-br from-pink-500 to-rose-600',
        'bg-gradient-to-br from-teal-500 to-cyan-600',
        'bg-gradient-to-br from-indigo-500 to-purple-600',
        'bg-gradient-to-br from-orange-500 to-red-600',
        'bg-gradient-to-br from-cyan-500 to-blue-600',
        'bg-gradient-to-br from-lime-500 to-green-600',
        'bg-gradient-to-br from-emerald-500 to-teal-600',
    ]
    
    if department_name:
        index = hash(department_name) % len(gradients)
        return gradients[index]
    return 'bg-gradient-to-br from-gray-500 to-gray-600'

@register.filter
def initials(employee):
    """
    Mengembalikan inisial dari employee (2 huruf) dari field nama dengan format yang cantik.
    - Jika nama terdiri dari 2 kata: ambil huruf pertama masing-masing
    - Jika 1 kata: ambil 2 huruf pertama
    - Jika 3+ kata: ambil huruf pertama kata pertama dan terakhir
    """
    nama = employee.nama or ''
    if not nama:
        return '??'
    
    # Bersihkan nama dari spasi berlebih
    nama = ' '.join(nama.split())
    parts = nama.split()
    
    if len(parts) >= 3:
        # Ambil huruf pertama kata pertama dan terakhir
        return (parts[0][0] + parts[-1][0]).upper()
    elif len(parts) == 2:
        # Ambil huruf pertama masing-masing kata
        return (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1:
        # Ambil dua huruf pertama
        name_part = parts[0]
        if len(name_part) >= 2:
            return name_part[:2].upper()
        else:
            # Kalau cuma 1 huruf, tambah '?'
            return (name_part[0] + '?').upper()
    
    return '??'

@register.filter
def initials_from_name(nama):
    """
    Versi alternatif yang menerima string nama langsung
    """
    if not nama:
        return '??'
    
    nama = ' '.join(nama.split())
    parts = nama.split()
    
    if len(parts) >= 3:
        return (parts[0][0] + parts[-1][0]).upper()
    elif len(parts) == 2:
        return (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1:
        if len(parts[0]) >= 2:
            return parts[0][:2].upper()
        return (parts[0][0] + '?').upper()
    
    return '??'

@register.filter
def status_badge_class(status):
    """
    Mengembalikan kelas CSS untuk badge status dengan gradient
    """
    badges = {
        'active': 'bg-gradient-to-r from-green-500 to-emerald-600 text-white',
        'probation': 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white',
        'terminated': 'bg-gradient-to-r from-red-500 to-pink-600 text-white',
        'resigned': 'bg-gradient-to-r from-gray-500 to-gray-600 text-white',
        'retired': 'bg-gradient-to-r from-purple-500 to-violet-600 text-white',
        'kontrak': 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white',
        'tetap': 'bg-gradient-to-r from-green-500 to-emerald-600 text-white',
        'harian': 'bg-gradient-to-r from-amber-500 to-yellow-600 text-white',
    }
    return badges.get(status, 'bg-gradient-to-r from-gray-500 to-gray-600 text-white')

@register.filter
def status_icon(status):
    """
    Mengembalikan SVG icon untuk status tertentu
    """
    icons = {
        'active': """
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
        """,
        'probation': """
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
        """,
        'terminated': """
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
        """,
        'resigned': """
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clip-rule="evenodd" />
            </svg>
        """,
        'kontrak': """
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
                <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
            </svg>
        """,
    }
    return icons.get(status, '')

@register.filter
def format_phone(phone_number):
    """
    Memformat nomor telepon menjadi format yang lebih mudah dibaca
    Contoh: 081234567890 -> 0812-3456-7890
    """
    if not phone_number:
        return '-'
    
    # Hapus semua karakter non-digit
    phone = ''.join(filter(str.isdigit, phone_number))
    
    if len(phone) >= 12:
        return f"{phone[:4]}-{phone[4:8]}-{phone[8:]}"
    elif len(phone) >= 8:
        return f"{phone[:4]}-{phone[4:]}"
    elif len(phone) >= 4:
        return f"{phone[:4]}-{phone[4:]}"
    
    return phone_number

@register.filter
def format_date(date_value):
    """
    Memformat tanggal ke format Indonesia yang cantik
    Contoh: 2024-03-10 -> 10 Maret 2024
    """
    if not date_value:
        return '-'
    
    try:
        from datetime import datetime
        if isinstance(date_value, str):
            date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        else:
            date_obj = date_value
        
        bulan_indonesia = [
            'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
        ]
        
        return f"{date_obj.day} {bulan_indonesia[date_obj.month-1]} {date_obj.year}"
    except:
        return str(date_value)

@register.filter
def mask_ktp(no_ktp):
    """
    Menyembunyikan nomor KTP untuk privasi
    Contoh: 1234567890123456 -> 1234 **** **** 3456
    """
    if not no_ktp or len(no_ktp) < 8:
        return no_ktp
    
    return f"{no_ktp[:4]} **** **** {no_ktp[-4:]}"

@register.filter
def get_department_color(department_name):
    """
    Mengembalikan warna untuk department (untuk card header, dll)
    """
    colors = {
        'IT': 'from-blue-600 to-indigo-700',
        'HR': 'from-green-600 to-emerald-700',
        'Finance': 'from-yellow-600 to-orange-700',
        'Marketing': 'from-pink-600 to-rose-700',
        'Sales': 'from-purple-600 to-violet-700',
        'Production': 'from-red-600 to-pink-700',
        'Warehouse': 'from-teal-600 to-cyan-700',
    }
    
    if department_name in colors:
        return colors[department_name]
    
    # Default random color based on hash
    default_gradients = [
        'from-blue-600 to-indigo-700',
        'from-green-600 to-emerald-700',
        'from-yellow-600 to-orange-700',
        'from-pink-600 to-rose-700',
        'from-purple-600 to-violet-700',
    ]
    index = hash(department_name) % len(default_gradients) if department_name else 0
    return default_gradients[index]

@register.filter
def age(birth_date):
    """
    Menghitung umur dari tanggal lahir
    """
    if not birth_date:
        return '-'
    
    from datetime import date
    today = date.today()
    
    if isinstance(birth_date, str):
        from datetime import datetime
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return f"{age} tahun"

@register.simple_tag
def department_icon(department_name):
    """
    Mengembalikan icon SVG untuk department tertentu
    """
    icons = {
        'IT': 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 5h10a2 2 0 012 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2z',
        'HR': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
        'Finance': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        'Marketing': 'M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z',
        'Production': 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    }
    
    path = icons.get(department_name, 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7c0-2.21-3.582-4-8-4s-8 1.79-8 4z')
    return f'<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{path}"></path></svg>'