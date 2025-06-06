document.addEventListener('DOMContentLoaded', function () {
    const modalProfesor = document.getElementById('confirmarEliminacionProfesorModal');
    modalProfesor.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');

        const form = modalProfesor.querySelector('#formEliminarProfesor');
        const nombreSpan = modalProfesor.querySelector('#nombreProfesorEliminar');

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
                    Swal.fire({
                        icon: 'success',
                        title: 'Usuario eliminado correctamente',
                        text: `El usuario ${nombre} ha sido eliminado.`,
                        confirmButtonText: 'Entendido',
                        confirmButtonColor: '#28a745'
                    }).then(() => {
                        location.reload(); // Recarga la página después de confirmar
                    });
                } else {
                    const data = await response.json();
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al eliminar el usuario',
                        html: `No se pudo eliminar el usuario. Detalles:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
                        confirmButtonText: 'Entendido',
                        confirmButtonColor: '#d33'
                    });
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error inesperado',
                    text: 'Ocurrió un error al intentar eliminar el usuario.',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#d33'
                });
            }
        });
    });
});


