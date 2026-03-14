// employee-modal.js - VERSI FINAL

console.log('🔥 employee-modal.js loaded');

// Pastikan tidak ada bentrok dengan deklarasi lain
if (typeof window.currentEmployeeId === 'undefined') {
    window.currentEmployeeId = null;
}

// Tab templates
const tabTemplates = {
    personal: (data) => `...`,  // isi dengan template yang sudah ada
    employment: (data) => `...`,
    bank: (data) => `...`
};

// Fungsi global
window.openModal = function(employeeId) {
    console.log('openModal dipanggil dengan ID:', employeeId);
    
    const modal = document.getElementById('employeeModal');
    if (!modal) {
        console.error('Modal tidak ditemukan!');
        return;
    }
    
    window.currentEmployeeId = employeeId;
    
    // Tampilkan modal
    modal.classList.remove('hidden');
    const loadingEl = document.getElementById('modalLoading');
    const contentEl = document.getElementById('modalContent');
    
    if (loadingEl) loadingEl.classList.remove('hidden');
    if (contentEl) {
        contentEl.classList.add('hidden');
        contentEl.innerHTML = '';
    }
    
    // Fetch data
    fetch(`/hr/employees/${employeeId}/detail/`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                if (loadingEl) loadingEl.classList.add('hidden');
                if (contentEl) {
                    contentEl.classList.remove('hidden');
                    window.currentEmployeeData = result.data;
                    window.switchTab('personal');
                }
            } else {
                alert('Gagal mengambil data');
                window.closeModal();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Terjadi kesalahan');
            window.closeModal();
        });
};

window.closeModal = function() {
    const modal = document.getElementById('employeeModal');
    if (modal) modal.classList.add('hidden');
};

window.switchTab = function(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400');
        btn.classList.add('border-transparent', 'text-gray-500');
    });
    
    const activeTab = document.getElementById(`tab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`);
    if (activeTab) {
        activeTab.classList.add('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400');
    }
    
    // Render tab content
    if (window.currentEmployeeData && tabTemplates[tabName]) {
        document.getElementById('modalContent').innerHTML = tabTemplates[tabName](window.currentEmployeeData);
    }
};

window.editEmployee = function() {
    alert('Fitur edit dummy');
};

// Pasang event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM siap');
    
    // Pasang listener ke semua element dengan data-nik
    const elements = document.querySelectorAll('[data-nik]');
    console.log('Ditemukan', elements.length, 'element dengan data-nik');
    
    elements.forEach(function(el) {
        // Hapus semua onclick lama
        el.removeAttribute('onclick');
        
        // Pasang event listener baru
        el.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const nik = this.getAttribute('data-nik');
            console.log('Element diklik, NIK:', nik);
            window.openModal(nik);
        });
    });
    
    // Tutup modal saat backdrop diklik
    const backdrop = document.getElementById('modalBackdrop');
    if (backdrop) {
        backdrop.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            window.closeModal();
        });
    }
});