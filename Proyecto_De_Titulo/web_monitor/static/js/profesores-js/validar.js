document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formulario_profesor');
    const rutInput = document.getElementById('rut_profesor');
    const rutError = document.getElementById('rut-error');
    const correoInput = document.getElementById('correo_profesor');
    const correoError = document.getElementById('correo-error');
    const nombreInput = document.getElementById('nombre_profesor');
    const nombreError = document.getElementById('nombre-error');
    const apellidoInput = document.getElementById('apellido_profesor');
    const apellidoError = document.getElementById('apellido-error');
    const alturaInput = document.getElementById('altura');
    const alturaError = document.getElementById('altura-error');
    const pesoInput = document.getElementById('peso');
    const pesoError = document.getElementById('peso-error');
    const antecedentesInput = document.getElementById('antecedentes_medicos');
    const antecedentesError = document.getElementById('antecedentes-error');
    const areaDocenciaInput = document.getElementById('area_docencia');
    const areaDocenciaError = document.getElementById('area-docencia-error');



    // Validar RUT
    rutInput.addEventListener('input', function () {
        const rut = rutInput.value;
        const regex = /^(\d{1,2}.\d{3}.\d{3}-[0-9Kk]|\d{7,8}-[0-9Kk])$/;
        if (!regex.test(rut)) {
            rutError.textContent = 'Formato de RUT inválido';
        } else {
            rutError.textContent = '';
        }
    });

    // Validar correo electrónico
    correoInput.addEventListener('input', function () {
        const valor = correoInput.value;
        const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!patron.test(valor)) {
            correoError.textContent = 'Correo electrónico inválido';
        } else {
            correoError.textContent = '';
        }
    });

    // Validar nombre
    nombreInput.addEventListener('input', function () {
        const nombre = nombreInput.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/u;
        if (!patron.test(nombre)) {
            nombreError.textContent = 'Nombre inválido';
        } else {
            nombreError.textContent = '';
        }
    });

    // Validar apellido
    apellidoInput.addEventListener('input', function () {
        const apellido = apellidoInput.value.trim();
        const patron = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
        if (!patron.test(apellido)) {
            apellidoError.textContent = 'Apellido inválido';
        } else {
            apellidoError.textContent = '';
        }
    });

    // Validar altura
    alturaInput.addEventListener('input', function () {
        const altura = alturaInput.value;
        const patron = /^\d{1,3}$/;
        if (!patron.test(altura) || parseInt(altura) < 50 || parseInt(altura) > 250) {
            alturaError.textContent = 'Altura inválida (debe ser entre 50 y 250 cm)';
        } else {
            alturaError.textContent = '';
        }
    });

    // Validar peso
    pesoInput.addEventListener('input', function () {
        const peso = pesoInput.value;
        const patron = /^\d{1,3}$/;
        if (!patron.test(peso) || parseInt(peso) < 20 || parseInt(peso) > 300) {
            pesoError.textContent = 'Peso inválido (debe ser entre 20 y 300 kg)';
        } else {
            pesoError.textContent = '';
        }
    });

    //  Validar antecedentes debe ser texto y tener minimo de 3 y maximo de 300
    antecedentesInput.addEventListener('input', function () {
        const antecedentes = antecedentesInput.value.trim();
        if (antecedentes.length < 3 || antecedentes.length > 300) {
            antecedentesError.textContent = 'Antecedentes deben tener entre 3 y 300 caracteres';
        } else {
            antecedentesError.textContent = '';
        }
    });
    
    // Validar area docencia
    areaDocenciaInput.addEventListener('input', function () {
        const areaDocencia = areaDocenciaInput.value.trim();
        if (areaDocencia.length < 3 || areaDocencia.length > 100) {
            areaDocenciaError.textContent = 'Área de docencia debe tener entre 3 y 100 caracteres';
        } else {
            areaDocenciaError.textContent = '';
        }
    });



    formulario.addEventListener('submit', function (event) {
        let esValido = true;
        let camposInvalidos = [];

        // Verificar errores en cada campo
        if (rutError.textContent) {
            esValido = false;
            camposInvalidos.push('RUT');
        }
        if (correoError.textContent) {
            esValido = false;
            camposInvalidos.push('Correo electrónico');
        }
        if (nombreError.textContent) {
            esValido = false;
            camposInvalidos.push('Nombre');
        }
        if (apellidoError.textContent) {
            esValido = false;
            camposInvalidos.push('Apellido');
        }
        if (alturaError.textContent) {
            esValido = false;
            camposInvalidos.push('Altura');
        }
        if (pesoError.textContent) {
            esValido = false;
            camposInvalidos.push('Peso');
        }
        if (antecedentesError.textContent) {
            esValido = false;
            camposInvalidos.push('Antecedentes médicos');
        }
        if (areaDocenciaError.textContent) {
            esValido = false;
            camposInvalidos.push('Área de docencia');
        }

        // Prevenir envío si hay errores
        if (!esValido) {
            event.preventDefault(); // Detiene el envío del formulario
            event.stopPropagation(); // Evita que otros manejadores de eventos se ejecuten

            // Usar SweetAlert2 para mostrar la alerta con los campos inválidos
            Swal.fire({
                icon: 'error',
                title: 'Errores al ingregar los datos',
                html: `Por favor, corrige los siguientes campos antes de enviar el formulario:<br><ul>${camposInvalidos.map(campo => `<li>${campo}</li>`).join('')}</ul>`,
                confirmButtonText: 'Entendido',
                confirmButtonColor: '#d33'
            });
        }
    });
});