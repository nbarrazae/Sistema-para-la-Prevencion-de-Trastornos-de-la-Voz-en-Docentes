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
                    console.log('Institución eliminada correctamente'); // Depuración
                    Swal.fire({
                        icon: 'success',
                        title: 'Institución eliminada correctamente',
                        text: `La institución ${nombre} ha sido eliminada.`,
                        confirmButtonText: 'Entendido',
                        confirmButtonColor: '#28a745'
                    }).then(() => {
                        location.reload(); // Recarga la página después de confirmar
                    });
                } else {
                    const data = await response.json();
                    console.log('Error al eliminar la institución:', data); // Depuración
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al eliminar la institución',
                        html: `No se pudo eliminar la institución. Detalles:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
                        confirmButtonText: 'Entendido',
                        confirmButtonColor: '#d33'
                    });
                }
            } catch (error) {
                console.error('Error inesperado:', error); // Depuración
                Swal.fire({
                    icon: 'error',
                    title: 'Error inesperado',
                    text: 'Ocurrió un error al intentar eliminar la institución.',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#d33'
                });
            }
        });
    });
});
