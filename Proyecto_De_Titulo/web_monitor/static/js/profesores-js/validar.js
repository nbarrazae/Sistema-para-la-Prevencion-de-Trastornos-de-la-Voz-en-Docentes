document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formulario_profesor');
    const modalAgregarProfesor = new bootstrap.Modal(document.getElementById('modalAgregarProfesor'));
    const cancelarModal = document.getElementById('cancelarModal');
    const modalEditarProfesor = new bootstrap.Modal(document.getElementById('modalEditarProfesor'));
    const cancelarModalEditar = document.getElementById('cancelarModalEditar');

    // Evento para cerrar el modal al hacer clic en "Cancelar" (Agregar)
    cancelarModal.addEventListener('click', function () {
        modalAgregarProfesor.hide(); // Cierra el modal
    });

    // Evento para cerrar el modal al hacer clic en "Cancelar" (Editar)
    cancelarModalEditar.addEventListener('click', function () {
        modalEditarProfesor.hide(); // Cierra el modal
    });

    // Asegúrate de que el evento submit se registre solo una vez
    if (formulario.dataset.iniciado === 'true') {
        return; // Evita registrar el evento más de una vez
    }
    formulario.dataset.iniciado = 'true';
        

    const campos = {
        rut: { input: document.getElementById('rut_profesor'), error: document.getElementById('rut-error') },
        correo: { input: document.getElementById('correo_profesor'), error: document.getElementById('correo-error') },
        nombre: { input: document.getElementById('nombre_profesor'), error: document.getElementById('nombre-error') },
        apellido: { input: document.getElementById('apellido_profesor'), error: document.getElementById('apellido-error') },
        altura: { input: document.getElementById('altura'), error: document.getElementById('altura-error') },
        peso: { input: document.getElementById('peso'), error: document.getElementById('peso-error') },
        antecedentes: { input: document.getElementById('antecedentes_medicos'), error: document.getElementById('antecedentes-error') },
        areaDocencia: { input: document.getElementById('area_docencia'), error: document.getElementById('area-docencia-error') }
    };

    const limpiarErrores = () => {
        for (let campo in campos) {
            campos[campo].error.textContent = '';
        }
    };

    // Funciones de validación individuales
    const validarRut = () => {
        const rut = campos.rut.input.value.trim();
        const regex = /^(\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]|\d{7,8}-[0-9Kk])$/;
        campos.rut.error.textContent = regex.test(rut) ? '' : 'Formato de RUT inválido';
    };

    const validarCorreo = () => {
        const correo = campos.correo.input.value.trim();
        const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        campos.correo.error.textContent = patron.test(correo) ? '' : 'Correo electrónico inválido';
    };

    const validarNombre = () => {
        const nombre = campos.nombre.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/u;

        if (nombre.length < 2) {
            campos.nombre.error.textContent = 'El nombre debe tener mínimo 2 caracteres';
        } else if (nombre.length > 50) {
            campos.nombre.error.textContent = 'El nombre debe tener máximo 50 caracteres';
        } else if (!patron.test(nombre)) {
            campos.nombre.error.textContent = 'Nombre inválido';
        } else {
            campos.nombre.error.textContent = '';
        }
    };

    const validarApellido = () => {
        const apellido = campos.apellido.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/u;

        if (apellido.length < 2) {
            campos.apellido.error.textContent = 'El apellido debe tener mínimo 2 caracteres';
        } else if (apellido.length > 50) {
            campos.apellido.error.textContent = 'El apellido debe tener máximo 50 caracteres';
        } else if (!patron.test(apellido)) {
            campos.apellido.error.textContent = 'Apellido inválido';
        } else {
            campos.apellido.error.textContent = '';
        }
    };

    const validarAltura = () => {
        const altura = parseInt(campos.altura.input.value, 10);
        if (!Number.isInteger(altura)) {
            campos.altura.error.textContent = 'La altura debe ser un número entero';
        } else if (altura < 50) {
            campos.altura.error.textContent = 'La altura debe ser al menos 50 cm';
        } else if (altura > 250) {
            campos.altura.error.textContent = 'La altura no puede superar los 250 cm';
        } else {
            campos.altura.error.textContent = '';
        }
    };

    const validarPeso = () => {
        const peso = parseFloat(campos.peso.input.value);
        if (isNaN(peso)) {
            campos.peso.error.textContent = 'El peso debe ser un número válido';
        } else if (peso < 20) {
            campos.peso.error.textContent = 'El peso debe ser al menos 20 kg';
        } else if (peso > 300) {
            campos.peso.error.textContent = 'El peso no puede superar los 300 kg';
        } else {
            campos.peso.error.textContent = '';
        }
    };

    const validarAntecedentes = () => {
        const texto = campos.antecedentes.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,0-9]+$/u;

        if (texto.length < 3) {
            campos.antecedentes.error.textContent = 'Antecedentes deben tener mínimo 3 caracteres';
        } else if (texto.length > 300) {
            campos.antecedentes.error.textContent = 'Antecedentes deben tener máximo 300 caracteres';
        } else if (!patron.test(texto)) {
            campos.antecedentes.error.textContent = 'Antecedentes contienen caracteres inválidos';
        } else {
            campos.antecedentes.error.textContent = '';
        }
    };

    const validarAreaDocencia = () => {
        const texto = campos.areaDocencia.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,0-9]+$/u;

        if (texto.length < 3) {
            campos.areaDocencia.error.textContent = 'Área de docencia debe tener mínimo 3 caracteres';
        } else if (texto.length > 100) {
            campos.areaDocencia.error.textContent = 'Área de docencia debe tener máximo 100 caracteres';
        } else if (!patron.test(texto)) {
            campos.areaDocencia.error.textContent = 'Área de docencia contiene caracteres inválidos';
        } else {
            campos.areaDocencia.error.textContent = '';
        }
    };

    // Asignar listeners a los inputs
    campos.rut.input.addEventListener('input', validarRut);
    campos.correo.input.addEventListener('input', validarCorreo);
    campos.nombre.input.addEventListener('input', validarNombre);
    campos.apellido.input.addEventListener('input', validarApellido);
    campos.altura.input.addEventListener('input', validarAltura);
    campos.peso.input.addEventListener('input', validarPeso);
    campos.antecedentes.input.addEventListener('input', validarAntecedentes);
    campos.areaDocencia.input.addEventListener('input', validarAreaDocencia);


    formulario.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        limpiarErrores();

        // Ejecutar validaciones
        validarRut();
        validarCorreo();
        validarNombre();
        validarApellido();
        validarAltura();
        validarPeso();
        validarAntecedentes();
        validarAreaDocencia();

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
                    title: 'Profesor agregado correctamente',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#28a745'
                }).then(() => {
                    modalAgregarProfesor.hide();
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
