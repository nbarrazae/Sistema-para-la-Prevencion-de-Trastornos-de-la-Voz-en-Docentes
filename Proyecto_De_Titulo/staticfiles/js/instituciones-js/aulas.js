function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Busca la cookie que empiece con el nombre
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



document.addEventListener('DOMContentLoaded', function () {
    const modalAulas = document.getElementById('modalAulas');

    function cargarContenidoModal(institucionId) {
      const contenido = modalAulas.querySelector('#contenidoAulas');
      contenido.innerHTML = `
        <div class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>`;

      fetch(`/institucion/${institucionId}/aulas/`)
        .then(response => response.json())
        .then(data => {
          contenido.innerHTML = data.html;
          asignarEventosAgregar(institucionId);
          asignarEventosModificar();
          asignarEventosEliminar(institucionId);
        });
    }

    function asignarEventosAgregar(institucionId) {
      const btnAgregar = document.getElementById('agregarAula');
      if (btnAgregar) {
      btnAgregar.addEventListener('click', function () {
        const tabla = document.getElementById('tablaAulas');
        const nuevaFila = document.createElement('tr');
        nuevaFila.innerHTML = `
        <td><input type="text" class="form-control text-center" name="nro_aula" style="width:90% ;"></td>
        <td><input type="text" class="form-control text-center" name="tamanio" style="width:90%;"></td>
        <td><input type="text" class="form-control text-center" name="cantidad_alumnos" style="width:90%;"></td>
        <td><input type="text" class="form-control text-center" name="descripcion" style="width:90%;"></td>
        <td><button class="btn btn-success btn-sm guardar-aula">Guardar</button></td>
        `;
        tabla.appendChild(nuevaFila);

          nuevaFila.querySelector('.guardar-aula').addEventListener('click', function () {
            const nro_aula = nuevaFila.querySelector('[name="nro_aula"]').value;
            const tamanio = nuevaFila.querySelector('[name="tamanio"]').value;
            const cantidad_alumnos = nuevaFila.querySelector('[name="cantidad_alumnos"]').value;
            const descripcion = nuevaFila.querySelector('[name="descripcion"]').value;

            fetch(`/institucion/${institucionId}/aulas/agregar/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify({
                nro_aula,
                tamanio,
                cantidad_alumnos,
                descripcion
              })
            })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                // Recargar contenido y re-asignar eventos
                cargarContenidoModal(institucionId);
              } else {
                alert('Error al guardar aula');
              }
            })
            .catch(error => {
              console.error('Error en fetch:', error);
              alert('Error al guardar aula');
            });
          });
        });
      }
    }

    function asignarEventosModificar() {
const botonesModificar = document.querySelectorAll('.modificar-aula');
botonesModificar.forEach(btn => {
  btn.addEventListener('click', function () {
    const fila = btn.closest('tr');
    const isEditando = btn.textContent === "Guardar";

    if (isEditando) {
      // Guardar datos
      const nro_aula = fila.querySelector('[name="nro_aula"]').value;
      const tamanio = fila.querySelector('[name="tamanio"]').value;
      const cantidad = fila.querySelector('[name="cantidad_alumnos"]').value;
      const descripcion = fila.querySelector('[name="descripcion"]').value;
      const id = btn.getAttribute('data-id');

      fetch(`/institucion/aula/${id}/modificar/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          nro_aula,
          tamanio,
          cantidad_alumnos: cantidad,
          descripcion
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          fila.innerHTML = `
            <td>${nro_aula}</td>
            <td>${tamanio}</td>
            <td>${cantidad}</td>
            <td>${descripcion}</td>
            <td>
              <button class="btn btn-primary btn-sm modificar-aula" data-id="${id}">Modificar</button>
              <button class="btn btn-danger btn-sm eliminar-aula" data-id="${id}">Eliminar</button>
            </td>`;
          asignarEventosModificar(); // Reasignar eventos
          asignarEventosEliminar();
        } else {
          alert("Error al guardar cambios");
        }
      });
    } else {
      // Cambiar a modo edición
      const celdas = fila.querySelectorAll('td');
      const nro_aula = celdas[0].textContent.trim();
      const tamanio = celdas[1].textContent.trim();
      const cantidad = celdas[2].textContent.trim();
      const descripcion = celdas[3].textContent.trim();

      fila.innerHTML = `
  <td><input class="form-control" type="text" name="nro_aula" value="${nro_aula}" /></td>
  <td><input class="form-control" type="text" name="tamanio" value="${tamanio}" /></td>
  <td><input class="form-control" type="text" name="cantidad_alumnos" value="${cantidad}" /></td>
  <td><input class="form-control" type="text" name="descripcion" value="${descripcion}" /></td>
  <td>
    <button class="btn btn-success btn-sm modificar-aula" data-id="${btn.getAttribute('data-id')}">Guardar</button>
    <button class="btn btn-danger btn-sm eliminar-aula" data-id="${btn.getAttribute('data-id')}" style="display: none;">Eliminar</button>
  </td>`;

      asignarEventosModificar(); // Reasignar para los nuevos botones
    }
  });
});
}

function asignarEventosEliminar(institucionId) {
const botonesEliminar = document.querySelectorAll('.eliminar-aula');

botonesEliminar.forEach(btn => {
  btn.addEventListener('click', function () {
    const id = btn.getAttribute('data-id');

    if (confirm('¿Estás seguro de que quieres eliminar esta aula?')) {
      fetch(`/institucion/aula/${id}/eliminar/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const institucionId = modalAulas.getAttribute('data-institucion-id'); // ← Aquí recuperas el ID
          cargarContenidoModal(institucionId);
        } else {
          alert('No se pudo eliminar el aula');
        }
      })
      .catch(error => {
        console.error('Error eliminando aula:', error);
        alert('Error al intentar eliminar el aula');
      });
    }
  });
});
}


    modalAulas.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const institucionId = button.getAttribute('data-institucion-id');
      modalAulas.setAttribute('data-institucion-id', institucionId);
      cargarContenidoModal(institucionId);
      
    });
  });