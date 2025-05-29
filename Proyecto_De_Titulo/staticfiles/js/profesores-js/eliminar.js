document.addEventListener('DOMContentLoaded', function () {
    const modalProfesor = document.getElementById('confirmarEliminacionProfesorModal');
    modalProfesor.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');
        const nombre = button.getAttribute('data-nombre');

        const form = modalProfesor.querySelector('#formEliminarProfesor');
        const nombreSpan = modalProfesor.querySelector('#nombreProfesorEliminar');

        form.action = url;
        nombreSpan.textContent = nombre;
    });
});
