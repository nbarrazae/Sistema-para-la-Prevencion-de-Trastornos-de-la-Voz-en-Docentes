
document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscadorInstituciones');
    const tabla = document.getElementById('tablaInstituciones');

    if (buscador && tabla) {
        buscador.addEventListener('input', function () {
            const filtro = buscador.value.toLowerCase();
            const filas = tabla.querySelectorAll('tbody tr');

            filas.forEach(fila => {
                const nombre = fila.querySelector('.nombre')?.textContent.toLowerCase() || '';
                const rut = fila.querySelector('.rut')?.textContent.toLowerCase() || '';
                const coincide = nombre.includes(filtro) || rut.includes(filtro);

                fila.style.display = coincide ? '' : 'none';
            });
        });
    }
});