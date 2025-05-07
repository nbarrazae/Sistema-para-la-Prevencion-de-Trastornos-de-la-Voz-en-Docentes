
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('confirmarEliminacionModal');
    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');
        
        const form = modal.querySelector('#formEliminar');
        const nombreSpan = modal.querySelector('#nombreInstitucionEliminar');
        
        form.action = url;
        nombreSpan.textContent = nombre;
    });
});
