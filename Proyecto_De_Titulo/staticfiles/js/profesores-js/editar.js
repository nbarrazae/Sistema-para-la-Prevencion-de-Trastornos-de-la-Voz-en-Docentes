document.addEventListener('DOMContentLoaded', function () {
    const modalEditar = document.getElementById('modalEditarProfesor');

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
        modalEditar.querySelector('form').action = url;
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
});
