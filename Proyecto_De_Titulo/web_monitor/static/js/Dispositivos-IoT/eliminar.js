document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('confirmarEliminacionModal');
    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const dispositivo = button.getAttribute('data-dispositivo');
        
        const form = modal.querySelector('#formEliminar');
        const dispositivoSpan = modal.querySelector('#nombreDispositivoEliminar');
        
        form.action = url;
        dispositivoSpan.textContent = dispositivo;
    });
});
