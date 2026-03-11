/**
 * Employee List JavaScript - GMT Repack
 * Handles all interactive features for employee list page
 */

class EmployeeList {
    constructor() {
        this.searchTimeout = null;
        this.searchInput = document.getElementById('searchInput');
        this.searchSpinner = document.getElementById('searchSpinner');
        this.contentContainer = document.getElementById('contentContainer');
        this.loadingSkeleton = document.getElementById('loadingSkeleton');
        this.viewMode = document.querySelector('[name="view"]')?.value || 'table';
        
        this.init();
    }

    init() {
        this.initSearch();
        this.initHoverCards();
        this.initColumnVisibility();
        this.initExportDropdown();
        this.initFilterModal();
        this.initViewToggle();
        this.initSorting();
    }

    /* ------------------------------------------------------------------------
       Search dengan Debounce
       ------------------------------------------------------------------------ */
    initSearch() {
        if (!this.searchInput) return;

        this.searchInput.addEventListener('input', () => {
            clearTimeout(this.searchTimeout);
            const query = this.searchInput.value;

            // Tampilkan spinner
            if (this.searchSpinner) {
                this.searchSpinner.classList.remove('hidden');
            }

            // Sembunyikan konten, tampilkan skeleton
            if (this.contentContainer && this.loadingSkeleton) {
                this.contentContainer.classList.add('hidden');
                this.loadingSkeleton.classList.remove('hidden');
            }

            this.searchTimeout = setTimeout(() => {
                this.performSearch(query);
            }, 500); // Debounce 500ms
        });
    }

    async performSearch(query) {
        const currentUrl = new URL(window.location.href);
        const params = new URLSearchParams(currentUrl.search);

        // Update search param
        if (query) {
            params.set('search', query);
        } else {
            params.delete('search');
        }
        params.set('page', '1'); // Reset ke halaman 1

        try {
            // Fetch dengan AJAX
            const response = await fetch(`/hr/employees/?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const html = await response.text();

            // Update URL tanpa reload
            window.history.pushState({}, '', `/hr/employees/?${params.toString()}`);

            // Update content
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.getElementById('contentContainer').innerHTML;
            
            if (this.contentContainer) {
                this.contentContainer.innerHTML = newContent;
            }

            // Sembunyikan skeleton, tampilkan konten
            if (this.loadingSkeleton) {
                this.loadingSkeleton.classList.add('hidden');
            }
            if (this.contentContainer) {
                this.contentContainer.classList.remove('hidden');
            }
            if (this.searchSpinner) {
                this.searchSpinner.classList.add('hidden');
            }

            // Re-attach event listeners
            this.initHoverCards();

        } catch (error) {
            console.error('Search error:', error);
            if (this.loadingSkeleton) {
                this.loadingSkeleton.classList.add('hidden');
            }
            if (this.contentContainer) {
                this.contentContainer.classList.remove('hidden');
            }
            if (this.searchSpinner) {
                this.searchSpinner.classList.add('hidden');
            }
        }
    }

    /* ------------------------------------------------------------------------
       Hover Card Preview
       ------------------------------------------------------------------------ */
    initHoverCards() {
        document.querySelectorAll('.hover-card').forEach(card => {
            const preview = card.querySelector('.hover-preview');
            if (!preview) return;

            card.addEventListener('mousemove', (e) => {
                const x = e.clientX;
                const y = e.clientY;
                const previewWidth = preview.offsetWidth;
                const previewHeight = preview.offsetHeight;

                // Hitung posisi agar tidak keluar layar
                let left = x + 20;
                let top = y - previewHeight / 2;

                // Cek batas kanan
                if (left + previewWidth > window.innerWidth) {
                    left = x - previewWidth - 20;
                }

                // Cek batas atas
                if (top < 10) {
                    top = 10;
                }

                // Cek batas bawah
                if (top + previewHeight > window.innerHeight - 10) {
                    top = window.innerHeight - previewHeight - 10;
                }

                preview.style.left = left + 'px';
                preview.style.top = top + 'px';
                preview.style.display = 'block';
            });

            card.addEventListener('mouseleave', () => {
                preview.style.display = 'none';
            });
        });
    }

    /* ------------------------------------------------------------------------
       Column Visibility Toggle
       ------------------------------------------------------------------------ */
    initColumnVisibility() {
        const checkboxes = document.querySelectorAll('[data-column]');
        
        // Load saved preferences from localStorage
        this.loadColumnPreferences();

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const column = e.target.dataset.column;
                const cells = document.querySelectorAll(`[data-column="${column}"]`);
                
                cells.forEach(cell => {
                    cell.style.display = e.target.checked ? 'table-cell' : 'none';
                });

                // Save to localStorage
                this.saveColumnPreference(column, e.target.checked);
            });
        });
    }

    loadColumnPreferences() {
        const preferences = JSON.parse(localStorage.getItem('columnVisibility') || '{}');
        
        Object.keys(preferences).forEach(column => {
            const checkbox = document.querySelector(`[data-column="${column}"]`);
            if (checkbox) {
                checkbox.checked = preferences[column];
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                checkbox.dispatchEvent(event);
            }
        });
    }

    saveColumnPreference(column, isVisible) {
        const preferences = JSON.parse(localStorage.getItem('columnVisibility') || '{}');
        preferences[column] = isVisible;
        localStorage.setItem('columnVisibility', JSON.stringify(preferences));
    }

    /* ------------------------------------------------------------------------
       Export Dropdown
       ------------------------------------------------------------------------ */
    initExportDropdown() {
        const exportBtn = document.getElementById('exportBtn');
        const exportDropdown = document.getElementById('exportDropdown');

        if (exportBtn && exportDropdown) {
            exportBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                exportDropdown.classList.toggle('hidden');
            });

            // Close when clicking outside
            document.addEventListener('click', (e) => {
                if (!exportBtn.contains(e.target) && !exportDropdown.contains(e.target)) {
                    exportDropdown.classList.add('hidden');
                }
            });

            // Export handlers
            document.querySelectorAll('[data-export]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const format = e.target.dataset.export;
                    this.exportData(format);
                });
            });
        }
    }

    exportData(format) {
        const currentUrl = new URL(window.location.href);
        const params = new URLSearchParams(currentUrl.search);
        
        // Add export format
        params.set('format', format);
        
        // Redirect to export URL
        window.location.href = `/hr/employees/export/?${params.toString()}`;
    }

    /* ------------------------------------------------------------------------
       Filter Modal
       ------------------------------------------------------------------------ */
    initFilterModal() {
        const modal = document.getElementById('filterModal');
        const openBtn = document.getElementById('openFilterModal');
        const closeBtn = document.getElementById('closeFilterModal');
        const cancelBtn = document.getElementById('cancelFilter');

        if (openBtn && modal) {
            openBtn.addEventListener('click', () => {
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        }

        if (closeBtn && modal) {
            closeBtn.addEventListener('click', () => this.closeFilterModal(modal));
        }

        if (cancelBtn && modal) {
            cancelBtn.addEventListener('click', () => this.closeFilterModal(modal));
        }

        // Close when clicking outside
        window.addEventListener('click', (e) => {
            if (modal && e.target === modal) {
                this.closeFilterModal(modal);
            }
        });

        // Initialize filter options
        this.loadFilterOptions();
    }

    closeFilterModal(modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }

    async loadFilterOptions() {
        try {
            const response = await fetch('/hr/employees/filter-options/');
            const data = await response.json();
            
            // Populate department select
            const deptSelect = document.getElementById('filterDepartment');
            if (deptSelect && data.departments) {
                data.departments.forEach(dept => {
                    const option = document.createElement('option');
                    option.value = dept.id;
                    option.textContent = dept.name;
                    deptSelect.appendChild(option);
                });
            }

            // Populate position select
            const posSelect = document.getElementById('filterPosition');
            if (posSelect && data.positions) {
                data.positions.forEach(pos => {
                    const option = document.createElement('option');
                    option.value = pos.id;
                    option.textContent = pos.title;
                    posSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading filter options:', error);
        }
    }

    /* ------------------------------------------------------------------------
       View Toggle (Table/Grid)
       ------------------------------------------------------------------------ */
    initViewToggle() {
        const viewToggles = document.querySelectorAll('.view-toggle-btn');
        
        viewToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                if (view) {
                    this.switchView(view);
                }
            });
        });
    }

    switchView(view) {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('view', view);
        window.location.href = currentUrl.toString();
    }

    /* ------------------------------------------------------------------------
       Sorting
       ------------------------------------------------------------------------ */
    initSorting() {
        const sortHeaders = document.querySelectorAll('[data-sort]');
        
        sortHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const sortBy = header.dataset.sort;
                const currentOrder = header.dataset.order || 'asc';
                const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
                
                const currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set('sort', sortBy);
                currentUrl.searchParams.set('order', newOrder);
                
                window.location.href = currentUrl.toString();
            });
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new EmployeeList();
});

// Handle browser back/forward
window.addEventListener('popstate', () => {
    window.location.reload();
});