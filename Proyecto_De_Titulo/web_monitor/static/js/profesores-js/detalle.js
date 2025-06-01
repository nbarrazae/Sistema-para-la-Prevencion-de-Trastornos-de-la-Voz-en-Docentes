document.addEventListener('DOMContentLoaded', function () {
    const modalDetalle = document.getElementById('modalDetalleProfesor');

    modalDetalle.addEventListener('show.bs.modal', function (event) {
        console.log('Modal Profesor se está abriendo');
        const button = event.relatedTarget;

        // Obtener atributos del botón que activó el modal
        const rut = button.getAttribute('data-rut');
        const correo = button.getAttribute('data-correo');
        const nombre = button.getAttribute('data-nombre');
        const apellido = button.getAttribute('data-apellido');
        const sexo = button.getAttribute('data-sexo');
        const institucion = button.getAttribute('data-institucion');
        const altura = button.getAttribute('data-altura');
        const peso = button.getAttribute('data-peso');
        const antecedentes = button.getAttribute('data-antecedentes');
        const area = button.getAttribute('data-area');

        // Asignar los valores al modal
        modalDetalle.querySelector('#detalleRut').textContent = rut || '—';
        modalDetalle.querySelector('#detalleCorreo').textContent = correo || '—';
        modalDetalle.querySelector('#detalleNombreApellido').textContent = `${nombre || '—'} ${apellido || '—'}`;
        modalDetalle.querySelector('#detalleSexo').textContent = sexo || '—';
        modalDetalle.querySelector('#detalleInstitucion').textContent = institucion || '—';
        modalDetalle.querySelector('#detalleAltura').textContent = altura || '—';
        modalDetalle.querySelector('#detallePeso').textContent = peso || '—';
        modalDetalle.querySelector('#detalleAntecedentes').textContent = antecedentes || '—';
        modalDetalle.querySelector('#detalleArea').textContent = area || '—';
    });
});
