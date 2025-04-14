
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
