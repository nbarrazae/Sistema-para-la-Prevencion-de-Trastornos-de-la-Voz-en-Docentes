
        const sidebar = document.getElementById('sidebar');
        const toggleBtn = document.getElementById('toggleSidebar');
        const toggleIcon = document.getElementById('toggleIcon');
    
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            // Cambia el icono
            if (sidebar.classList.contains('collapsed')) {
                toggleIcon.classList.remove('fa-angle-double-left');
                toggleIcon.classList.add('fa-angle-double-right');
            } else {
                toggleIcon.classList.remove('fa-angle-double-right');
                toggleIcon.classList.add('fa-angle-double-left');
            }
        });

    // ✅ Función para aplicar el estado guardado
    function applySidebarState() {
        const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (collapsed) {
            sidebar.classList.add('collapsed');
            toggleIcon.classList.remove('fa-angle-double-left');
            toggleIcon.classList.add('fa-angle-double-right');
        } else {
            sidebar.classList.remove('collapsed');
            toggleIcon.classList.remove('fa-angle-double-right');
            toggleIcon.classList.add('fa-angle-double-left');
        }
    }

    // ✅ Cambiar estado al hacer clic
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        const isCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', isCollapsed);

        // Cambiar icono
        toggleIcon.classList.toggle('fa-angle-double-left');
        toggleIcon.classList.toggle('fa-angle-double-right');
    });

    // ✅ Aplicar estado guardado al cargar la página
    document.addEventListener('DOMContentLoaded', applySidebarState);
