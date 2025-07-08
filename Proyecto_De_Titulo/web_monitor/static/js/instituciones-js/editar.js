document.addEventListener('DOMContentLoaded', function () {
    const modalEditar = document.getElementById('modalEditarInstitucion');
    const formularioEditar = modalEditar.querySelector('form');

    modalEditar.addEventListener('show.bs.modal', function (event) {
        console.log('Modal de edición abierto');

        const button = event.relatedTarget;

        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');
        const rut = button.getAttribute('data-rut');
        const direccion = button.getAttribute('data-direccion');
        const telefono = button.getAttribute('data-telefono');
        const correo = button.getAttribute('data-correo');
        const sitio_web = button.getAttribute('data-sitio_web');
        const representante_legal = button.getAttribute('data-representante_legal');

        formularioEditar.action = url;
        modalEditar.querySelector('#inputNombre').value = nombre;
        modalEditar.querySelector('#inputRut').value = rut;
        modalEditar.querySelector('#inputDireccion').value = direccion;
        modalEditar.querySelector('#inputTelefono').value = telefono;
        modalEditar.querySelector('#inputCorreo').value = correo;
        modalEditar.querySelector('#inputSitioWeb').value = sitio_web;
        modalEditar.querySelector('#inputRepresentanteLegal').value = representante_legal;
    });

    const campos = {
        nombre: { input: document.getElementById('inputNombre'), error: document.getElementById('editarNombre-error') },
        rut: { input: document.getElementById('inputRut'), error: document.getElementById('editarRut-error') },
        direccion: { input: document.getElementById('inputDireccion'), error: document.getElementById('editarDireccion-error') },
        telefono: { input: document.getElementById('inputTelefono'), error: document.getElementById('editarTelefono-error') },
        correo: { input: document.getElementById('inputCorreo'), error: document.getElementById('editarCorreo-error') },
        sitioWeb: { input: document.getElementById('inputSitioWeb'), error: document.getElementById('editarSitioWeb-error') },
        representanteLegal: { input: document.getElementById('inputRepresentanteLegal'), error: document.getElementById('editarRepresentanteLegal-error') }
    };

    const limpiarErrores = () => {
        for (let campo in campos) {
            campos[campo].error.textContent = '';
        }
    };

    // Funciones de validación 
    const validarNombre = () => {
        const nombre = campos.nombre.input.value.trim();
        const patron = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/;

        if (nombre.length < 2) {
            campos.nombre.error.textContent = 'El nombre debe tener mínimo 2 caracteres';
        } else if (nombre.length > 100) {
            campos.nombre.error.textContent = 'El nombre debe tener máximo 100 caracteres';
        } else if (!patron.test(nombre)) {
            campos.nombre.error.textContent = 'Nombre inválido';
        } else {
            campos.nombre.error.textContent = '';
        }
    };

    const validarRut = () => {
        const rut = campos.rut.input.value.trim();
        const patron = /^\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]$|^\d{7,8}-[0-9Kk]$/;
        campos.rut.error.textContent = !patron.test(rut) ? 'Formato de RUT inválido.' : '';
    };

    const validarDireccion = () => {
        const direccion = campos.direccion.input.value.trim();
        const patron = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/;

        if (direccion.length < 5) {
            campos.direccion.error.textContent = 'La dirección debe tener mínimo 5 caracteres';
        } else if (direccion.length > 100) {
            campos.direccion.error.textContent = 'La dirección debe tener máximo 100 caracteres';
        } else if (!patron.test(direccion)) {
            campos.direccion.error.textContent = 'Dirección inválida';
        } else {
            campos.direccion.error.textContent = '';
        }
    };

    const validarSitioWeb = () => {
        const sitioWeb = campos.sitioWeb.input.value.trim();
        const patron = /^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\/?.*$/;

        if (sitioWeb.length > 50) {
            campos.sitioWeb.error.textContent = 'El sitio web debe tener máximo 50 caracteres.';
        } else if (sitioWeb && !patron.test(sitioWeb)) {
            campos.sitioWeb.error.textContent = 'Sitio web inválido.';
        } else {
            campos.sitioWeb.error.textContent = '';
        }
    };

    const validarRepresentanteLegal = () => {
        const representanteLegal = campos.representanteLegal.input.value.trim();
        const patron = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/;

        if (representanteLegal.length < 2) {
            campos.representanteLegal.error.textContent = 'El representante legal debe tener mínimo 2 caracteres.';
        } else if (representanteLegal.length > 100) {
            campos.representanteLegal.error.textContent = 'El representante legal debe tener máximo 100 caracteres.';
        } else if (!patron.test(representanteLegal)) {
            campos.representanteLegal.error.textContent = 'Representante legal inválido.';
        } else {
            campos.representanteLegal.error.textContent = '';
        }
    };

    const validarTelefono = () => {
        const telefono = campos.telefono.input.value.trim();
        const patron = /^\+?56\s?9\s?\d{4}\s?\d{4}$|^\d{8,12}$/;
        campos.telefono.error.textContent = !patron.test(telefono) ? 'Teléfono inválido.' : '';
    };

    const validarCorreo = () => {
        const correo = campos.correo.input.value.trim();
        const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        campos.correo.error.textContent = !patron.test(correo) ? 'Correo electrónico inválido.' : '';
    };

    campos.nombre.input.addEventListener('input', validarNombre);
    campos.rut.input.addEventListener('input', validarRut);
    campos.direccion.input.addEventListener('input', validarDireccion);
    campos.sitioWeb.input.addEventListener('input', validarSitioWeb);
    campos.representanteLegal.input.addEventListener('input', validarRepresentanteLegal);
    campos.telefono.input.addEventListener('input', validarTelefono);
    campos.correo.input.addEventListener('input', validarCorreo);

    formularioEditar.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        limpiarErrores();

        validarNombre();
        validarRut();
        validarDireccion();
        validarSitioWeb();
        validarRepresentanteLegal();
        validarTelefono();
        validarCorreo();

        let esValido = true;
        let camposInvalidos = [];

        for (let campo in campos) {
            if (campos[campo].error.textContent) {
                esValido = false;
                const nombreCampo = campos[campo].input.getAttribute('data-label') || campo;
                camposInvalidos.push(nombreCampo.charAt(0).toUpperCase() + nombreCampo.slice(1));
            }
        }

        if (!esValido) {
            Swal.fire({
                icon: 'error',
                title: 'Errores al ingresar los datos',
                html: `Corrige los siguientes campos antes de enviar:<br><ul>${camposInvalidos.map(campo => `<li>${campo}</li>`).join('')}</ul>`,
                confirmButtonText: 'Entendido',
                confirmButtonColor: '#d33'
            });
            return;
        }

        const formData = new FormData(formularioEditar);
        try {
            const response = await fetch(formularioEditar.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const data = await response.json();
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Institucion editada correctamente',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#28a745'
                }).then(() => {
                    const bootstrapModal = bootstrap.Modal.getInstance(modalEditar);
                    bootstrapModal.hide();
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                });
            } else {
                const errores = Object.values(data.error).map(mensaje => `<li>${mensaje}</li>`).join('');
                Swal.fire({
                    icon: 'error',
                    title: 'Errores al ingresar los datos',
                    html: `Corrige los siguientes campos antes de enviar:<br><ul>${errores}</ul>`,
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#d33'
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error inesperado',
                text: 'Ocurrió un error al enviar los datos.',
                confirmButtonText: 'Entendido',
                confirmButtonColor: '#d33'
            });
        }
    });
});