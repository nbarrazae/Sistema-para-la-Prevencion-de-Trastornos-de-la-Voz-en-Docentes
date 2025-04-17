document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const icon = document.getElementById('toggleIcon');
    const container = document.getElementById('mainContainer');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const overlay = document.getElementById('overlay');

    // Restaurar estado
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed && window.innerWidth > 768) {
        sidebar.classList.add('collapsed');
        icon.classList.remove('fa-angle-double-left');
        icon.classList.add('fa-angle-double-right');
        container.classList.add('expanded');
    }

    // Botón escritorio
    toggleButton?.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        const collapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebar-collapsed', collapsed);

        icon?.classList.toggle('fa-angle-double-left', !collapsed);
        icon?.classList.toggle('fa-angle-double-right', collapsed);

        container.classList.toggle('expanded', collapsed);
    });

    // Botón hamburguesa móvil
    mobileMenuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('show');
    
        if (sidebar.classList.contains('show')) {
            mobileMenuBtn.style.display = 'none'; // Oculta botón
        } else {
            mobileMenuBtn.style.display = 'flex'; // Vuelve a mostrar si se cierra
        }
    });
    

    // Cerrar al tocar el overlay
    overlay?.addEventListener('click', () => {
        sidebar.classList.remove('show');
        overlay.style.display = 'none';
    });

    // Ocultar sidebar móvil al hacer clic en un link
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('show');
                mobileMenuBtn.style.display = 'flex'; // Mostrar botón de nuevo
            }
        });
    });

    document.addEventListener('click', (e) => {
        const isClickInsideSidebar = sidebar.contains(e.target);
        const isClickOnMobileBtn = mobileMenuBtn.contains(e.target);
    
        // Solo en móvil y si la barra está abierta
        if (window.innerWidth <= 768 && sidebar.classList.contains('show')) {
            if (!isClickInsideSidebar && !isClickOnMobileBtn) {
                sidebar.classList.remove('show');
                mobileMenuBtn.style.display = 'flex'; // Vuelve a mostrar el botón hamburguesa
            }
        }
    });
    
    
});
