
document.addEventListener('DOMContentLoaded', function () {
    const modalEditar = document.getElementById('modalEditarInstitucion');
    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');
        const rut = button.getAttribute('data-rut');
        const direccion = button.getAttribute('data-direccion');
        const sitio_web = button.getAttribute('data-sitio_web');
        const representante_legal = button.getAttribute('data-representante_legal');
        const telefono = button.getAttribute('data-telefono');
        const correo = button.getAttribute('data-correo');

        const form = modalEditar.querySelector('#formEditar');
        form.action = url;

        modalEditar.querySelector('#inputNombre').value = nombre;
        modalEditar.querySelector('#inputRut').value = rut;
        modalEditar.querySelector('#inputDireccion').value = direccion;
        modalEditar.querySelector('#inputSitioWeb').value = sitio_web;
        modalEditar.querySelector('#inputRepresentanteLegal').value = representante_legal;
        modalEditar.querySelector('#inputTelefono').value = telefono;
        modalEditar.querySelector('#inputCorreo').value = correo;
    });
});
