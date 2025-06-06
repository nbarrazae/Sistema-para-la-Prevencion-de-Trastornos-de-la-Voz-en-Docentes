document.addEventListener('DOMContentLoaded', function () {
    const modalEditar = document.getElementById('modalEditarProfesor');
    const formularioEditar = modalEditar.querySelector('form');

    modalEditar.addEventListener('show.bs.modal', function (event) {
        console.log('Modal de edición de profesor se está abriendo');

        const button = event.relatedTarget;

        // Extraer datos del botón
        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');
        const apellido = button.getAttribute('data-apellido');
        const rut = button.getAttribute('data-rut');
        const correo = button.getAttribute('data-correo');
        const sexo = button.getAttribute('data-sexo');
        const altura = button.getAttribute('data-altura');
        const peso = button.getAttribute('data-peso');
        const antecedentes = button.getAttribute('data-antecedentes');
        const area = button.getAttribute('data-area');
        const institucionId = button.getAttribute('data-institucion-id');

        // Asignar datos al formulario
        formularioEditar.action = url;
        modalEditar.querySelector('#editarNombre').value = nombre;
        modalEditar.querySelector('#editarApellido').value = apellido;
        modalEditar.querySelector('#editarRut').value = rut;
        modalEditar.querySelector('#editarCorreo').value = correo;
        modalEditar.querySelector('#editarSexo').value = sexo;
        modalEditar.querySelector('#editarAltura').value = altura;
        modalEditar.querySelector('#editarPeso').value = peso;
        modalEditar.querySelector('#editarAntecedentes').value = antecedentes;
        modalEditar.querySelector('#editarArea').value = area;
        modalEditar.querySelector('#editarInstitucion').value = institucionId;
    });

    const campos = {
        rut: { input: document.getElementById('editarRut'), error: document.getElementById('editarRut-error') },
        correo: { input: document.getElementById('editarCorreo'), error: document.getElementById('editarCorreo-error') },
        nombre: { input: document.getElementById('editarNombre'), error: document.getElementById('editarNombre-error') },
        apellido: { input: document.getElementById('editarApellido'), error: document.getElementById('editarApellido-error') },
        altura: { input: document.getElementById('editarAltura'), error: document.getElementById('editarAltura-error') },
        peso: { input: document.getElementById('editarPeso'), error: document.getElementById('editarPeso-error') },
        antecedentes: { input: document.getElementById('editarAntecedentes'), error: document.getElementById('editarAntecedentes-error') },
        areaDocencia: { input: document.getElementById('editarArea'), error: document.getElementById('editarArea-error') }
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

    // Asignar listeners a los inputs para validación en tiempo real
    campos.rut.input.addEventListener('input', validarRut);
    campos.correo.input.addEventListener('input', validarCorreo);
    campos.nombre.input.addEventListener('input', validarNombre);
    campos.apellido.input.addEventListener('input', validarApellido);
    campos.altura.input.addEventListener('input', validarAltura);
    campos.peso.input.addEventListener('input', validarPeso);
    campos.antecedentes.input.addEventListener('input', validarAntecedentes);
    campos.areaDocencia.input.addEventListener('input', validarAreaDocencia);

    formularioEditar.addEventListener('submit', async function (event) {
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
                    title: 'Profesor editado correctamente',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#28a745'
                }).then(() => {
                    // Cerrar el modal antes de recargar la página
                    const bootstrapModal = bootstrap.Modal.getInstance(modalEditar);
                    bootstrapModal.hide(); // Cierra el modal
                    setTimeout(() => {
                        location.reload(); // Recarga la página después de cerrar el modal
                    }, 2000); // Agregar un pequeño retraso para asegurar el cierre del modal
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