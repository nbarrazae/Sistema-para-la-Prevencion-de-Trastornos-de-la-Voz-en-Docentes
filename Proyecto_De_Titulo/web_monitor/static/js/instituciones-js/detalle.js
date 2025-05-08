
document.addEventListener('DOMContentLoaded', function () {
    const modalDetalle = document.getElementById('modalDetalleInstitucion');
    modalDetalle.addEventListener('show.bs.modal', function (event) {
        console.log('Modal se está abriendo'); // <-- Agrega esto temporalmente
        const button = event.relatedTarget;
        const nombre = button.getAttribute('data-nombre');
        const rut = button.getAttribute('data-rut');
        const direccion = button.getAttribute('data-direccion');
        const telefono = button.getAttribute('data-telefono');
        const correo = button.getAttribute('data-correo');
        const sitio_web = button.getAttribute('data-sitio_web');
        const representante_legal = button.getAttribute('data-representante_legal');
        const created_at = button.getAttribute('data-created_at');
        const updated_at = button.getAttribute('data-updated_at');


        modalDetalle.querySelector('#detalleNombre').textContent = nombre;
        modalDetalle.querySelector('#detalleRut').textContent = rut;
        modalDetalle.querySelector('#detalleDireccion').textContent = direccion;
        modalDetalle.querySelector('#detalleTelefono').textContent = telefono;
        modalDetalle.querySelector('#detalleCorreo').textContent = correo;
        modalDetalle.querySelector('#detalleSitioWeb').textContent = sitio_web;
        modalDetalle.querySelector('#detalleRepresentanteLegal').textContent = representante_legal;
        modalDetalle.querySelector('#detalleFechaCreacion').textContent = created_at;
        modalDetalle.querySelector('#detalleUltimaModificacion').textContent = updated_at;

    });
});
