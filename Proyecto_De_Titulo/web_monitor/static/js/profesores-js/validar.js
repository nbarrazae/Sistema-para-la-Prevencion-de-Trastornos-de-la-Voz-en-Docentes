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
        campos.nombre.error.textContent = patron.test(nombre) ? '' : 'Nombre inválido';
    };

    const validarApellido = () => {
        const apellido = campos.apellido.input.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/u;
        campos.apellido.error.textContent = patron.test(apellido) ? '' : 'Apellido inválido';
    };

    const validarAltura = () => {
        const altura = parseInt(campos.altura.input.value, 10);
        campos.altura.error.textContent = (!Number.isInteger(altura) || altura < 50 || altura > 250)
            ? 'Altura inválida (debe ser entre 50 y 250 cm)' : '';
    };

    const validarPeso = () => {
        const peso = parseInt(campos.peso.input.value, 10);
        campos.peso.error.textContent = (!Number.isInteger(peso) || peso < 20 || peso > 300)
            ? 'Peso inválido (debe ser entre 20 y 300 kg)' : '';
    };

    const validarAntecedentes = () => {
        const texto = campos.antecedentes.input.value.trim();
        campos.antecedentes.error.textContent = (texto.length < 3 || texto.length > 300)
            ? 'Antecedentes deben tener entre 3 y 300 caracteres' : '';
    };

    const validarAreaDocencia = () => {
        const texto = campos.areaDocencia.input.value.trim();
        campos.areaDocencia.error.textContent = (texto.length < 3 || texto.length > 100)
            ? 'Área de docencia debe tener entre 3 y 100 caracteres' : '';
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
                Swal.fire({
                    icon: 'error',
                    title: 'Errores al ingresar los datos',
                    html: `Corrige los siguientes campos antes de enviar:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
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
