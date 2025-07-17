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
    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Dispositivo eliminado correctamente',
                    text: `El dispositivo ${dispositivo} ha sido eliminado.`,
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#28a745'
                }).then(() => {
                    location.reload();
                });
            } else {
                const data = await response.json();
                Swal.fire({
                    icon: 'error',
                    title: 'Error al eliminar el dispositivo',
                    html: `No se pudo eliminar el dispositivo. Detalles:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#d33'
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error inesperado',
                text: 'Ocurrió un error al intentar eliminar el dispositivo.',
                confirmButtonText: 'Entendido',
                confirmButtonColor: '#d33'
            });
        }
    }, { once: true });
});
});
