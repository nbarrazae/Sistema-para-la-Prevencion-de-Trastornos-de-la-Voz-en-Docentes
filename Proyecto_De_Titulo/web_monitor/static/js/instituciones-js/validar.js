document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formulario_institucion');
    const modalAgregarInstitucion = new bootstrap.Modal(document.getElementById('modalAgregarInstitucion'));
    const cancelarModal = document.getElementById('cancelarModal');
    const modalEditarInstitucion = new bootstrap.Modal(document.getElementById('modalEditarInstitucion'));
    const cancelarModalEditar = document.getElementById('cancelarModalEditar');

    // Evento para cerrar el modal al hacer clic en "Cancelar" (Agregar)
    cancelarModal.addEventListener('click', function () {
        modalAgregarInstitucion.hide(); // Cierra el modal
    });

    // Evento para cerrar el modal al hacer clic en "Cancelar" (Editar)
    cancelarModalEditar.addEventListener('click', function () {
        modalEditarInstitucion.hide(); // Cierra el modal
    });

    const campos = {
        nombre: { input: document.getElementById('nombre_institucion'), error: document.getElementById('nombre-error') },
        rut: { input: document.getElementById('rut_institucion'), error: document.getElementById('rut-error') },
        direccion: { input: document.getElementById('direccion'), error: document.getElementById('direccion-error') },
        sitioWeb: { input: document.getElementById('sitio_web'), error: document.getElementById('sitio-web-error') },
        representanteLegal: { input: document.getElementById('representante_legal'), error: document.getElementById('representante-legal-error') },
        telefono: { input: document.getElementById('telefono_institucion'), error: document.getElementById('telefono-error') },
        correo: { input: document.getElementById('correo_institucion'), error: document.getElementById('correo-error') },
    };

    const limpiarErrores = () => {
        for (let campo in campos) {
            campos[campo].error.textContent = '';
        }
    };

    // Funciones de validación individuales
    const validarNombre = () => {
        const nombre = campos.nombre.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/;
        campos.nombre.error.textContent = patron.test(nombre) ? '' : 'Nombre inválido (mínimo 2 caracteres, solo letras y caracteres especiales).';
    };

    const validarRut = () => {
        const rut = campos.rut.input.value.trim();
        const patron = /^\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]$|^\d{7,8}-[0-9Kk]$/;
        campos.rut.error.textContent = patron.test(rut) ? '' : 'RUT inválido (formato XX.XXX.XXX-X o XXXXXXXX-X).';
    };

    const validarDireccion = () => {
        const direccion = campos.direccion.input.value.trim();
        const patron = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:\'"]+$/;
        campos.direccion.error.textContent = patron.test(direccion) ? '' : 'Dirección inválida (mínimo 5 caracteres).';
    };

    const validarSitioWeb = () => {
        const sitioWeb = campos.sitioWeb.input.value.trim();
        const patron = /^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\/?.*$/;
        campos.sitioWeb.error.textContent = sitioWeb === '' || patron.test(sitioWeb) ? '' : 'Sitio web inválido.';
    };

    const validarRepresentanteLegal = () => {
        const representanteLegal = campos.representanteLegal.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/;
        campos.representanteLegal.error.textContent = patron.test(representanteLegal) ? '' : 'Representante legal inválido (mínimo 2 caracteres).';
    };

    const validarTelefono = () => {
        const telefono = campos.telefono.input.value.trim();
        const patron = /^\+?56\s?9\s?\d{4}\s?\d{4}$|^\d{8,12}$/;
        campos.telefono.error.textContent = patron.test(telefono) ? '' : 'Teléfono inválido (formato +56 9 XXXX XXXX o XXXXXXXX).';
    };

    const validarCorreo = () => {
        const correo = campos.correo.input.value.trim();
        const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        campos.correo.error.textContent = patron.test(correo) ? '' : 'Correo electrónico inválido.';
    };

    // Asignar listeners a los inputs
    campos.nombre.input.addEventListener('input', validarNombre);
    campos.rut.input.addEventListener('input', validarRut);
    campos.direccion.input.addEventListener('input', validarDireccion);
    campos.sitioWeb.input.addEventListener('input', validarSitioWeb);
    campos.representanteLegal.input.addEventListener('input', validarRepresentanteLegal);
    campos.telefono.input.addEventListener('input', validarTelefono);
    campos.correo.input.addEventListener('input', validarCorreo);

    formulario.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        limpiarErrores();

        // Ejecutar validaciones
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

        const formData = new FormData(formulario);
        try {
            const response = await fetch(formulario.action, {
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
                    title: 'Institución agregada correctamente',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#28a745'
                }).then(() => {
                    modalAgregarInstitucion.hide();
                    location.reload();
                });
            } else {
                // Mostrar múltiples errores
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