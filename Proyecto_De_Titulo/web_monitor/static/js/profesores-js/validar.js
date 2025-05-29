
//  Validar Rut profesor formato XX.XXX.XXX-X o XXXXXXXX-X
document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut_profesor');
    const rutError = document.getElementById('rut-error');

    rutInput.addEventListener('input', function () {
        const rut = rutInput.value;
        const regex = /^(\d{1,2}.\d{3}.\d{3}-[0-9Kk]|\d{7,8}-[0-9Kk])$/;
        if (!regex.test(rut)) {
            rutError.textContent = 'Formato de RUT inválido';
        } else {
            rutError.textContent = '';
        }
    });
});

// Validar correo electrónico profesor
document.addEventListener('DOMContentLoaded', function () {
    const correoInput = document.getElementById('correo_profesor');
    const correoError = document.getElementById('correo-error');

    correoInput.addEventListener('input', function () {
        const valor = correoInput.value;
        const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!patron.test(valor)) {
            correoError.textContent = 'Correo electrónico inválido';
        } else {
            correoError.textContent = '';
        }
    });
});


// Validar nombre, solo letras y espacios
document.addEventListener('DOMContentLoaded', function () {
    const nombreInput = document.getElementById('nombre_profesor');
    const nombreError = document.getElementById('nombre-error');

    nombreInput.addEventListener('input', function () {
        const nombre = nombreInput.value;
        const patron = /^[a-zA-Z\s]+$/; // Solo letras y espacios
        if (!patron.test(nombre)) {
            nombreError.textContent = 'Nombre inválido';
        } else {
            nombreError.textContent = '';
        }
    });
}
);

// Validar nombre, solo letras y espacios
document.addEventListener('DOMContentLoaded', function () {
    const nombreInput = document.getElementById('editarNombre');
    const nombreError = document.getElementById('editarNombre-error');

    nombreInput.addEventListener('input', function () {
        const nombre = nombreInput.value;
        const patron = /^[a-zA-Z\s]+$/; // Solo letras y espacios
        if (!patron.test(nombre)) {
            nombreError.textContent = 'Nombre inválido';
        } else {
            nombreError.textContent = '';
        }
    });
}
);

// Validar apellido, solo letras y espacios
document.addEventListener('DOMContentLoaded', function () {
    const apellidoInput = document.getElementById('apellido_profesor');
    const apellidoError = document.getElementById('apellido-error');

    apellidoInput.addEventListener('input', function () {
        const apellido = apellidoInput.value;
        const patron = /^[a-zA-Z\s]+$/; // Solo letras y espacios
        if (!patron.test(apellido)) {
            apellidoError.textContent = 'Apellido inválido';
        } else {
            apellidoError.textContent = '';
        }
    });
}
);

// Validar Altura (cm)
document.addEventListener('DOMContentLoaded', function () {
    const alturaInput = document.getElementById('altura');
    const alturaError = document.getElementById('altura-error');

    alturaInput.addEventListener('input', function () {
        const altura = alturaInput.value;
        const patron = /^\d{1,3}$/; // Solo números de 1 a 3 dígitos
        if (!patron.test(altura) || parseInt(altura) < 50 || parseInt(altura) > 250) {
            alturaError.textContent = 'Altura inválida (debe ser entre 50 y 250 cm)';
        } else {
            alturaError.textContent = '';
        }
    });
});

// Validar Peso (kg)
document.addEventListener('DOMContentLoaded', function () {
    const pesoInput = document.getElementById('peso');
    const pesoError = document.getElementById('peso-error');

    pesoInput.addEventListener('input', function () {
        const peso = pesoInput.value;
        const patron = /^\d{1,3}$/; // Solo números de 1 a 3 dígitos
        if (!patron.test(peso) || parseInt(peso) < 20 || parseInt(peso) > 300) {
            pesoError.textContent = 'Peso inválido (debe ser entre 20 y 300 kg)';
        } else {
            pesoError.textContent = '';
        }
    });
});
