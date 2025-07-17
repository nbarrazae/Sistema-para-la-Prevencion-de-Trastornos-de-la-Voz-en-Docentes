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
        })
        .catch(error => {
          console.error('Error cargando aulas:', error);
          contenido.innerHTML = `
            <div class="alert alert-danger text-center">
              <i class="fas fa-exclamation-triangle"></i>
              <p class="mb-0">Error al cargar las aulas. Por favor, intenta nuevamente.</p>
            </div>`;
          
          Swal.fire({
            icon: 'error',
            title: 'Error al cargar aulas',
            text: 'No se pudieron cargar las aulas de la institución. Por favor, recarga la página e intenta nuevamente.',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#d33'
          });
        });
    }

    function asignarEventosAgregar(institucionId) {
      const btnAgregar = document.getElementById('agregarAula');
      if (btnAgregar) {
        btnAgregar.addEventListener('click', function () {
          // Evita duplicar filas de ingreso
          if (document.querySelector('#tablaAulas tr input')) return;
    
          const tabla = document.getElementById('tablaAulas');
          const nuevaFila = document.createElement('tr');
          nuevaFila.innerHTML = `
            <td>
              <input type="text" class="form-control" name="nro_aula" style="width:100px" placeholder="Ej: A-101">
              <small class="text-danger error-message" id="error-nro_aula"></small>
            </td>
            <td>
              <input type="number" class="form-control" name="tamanio" style="width:100px" placeholder="Ej: 50" min="1">
              <small class="text-danger error-message" id="error-tamanio"></small>
            </td>
            <td>
              <input type="number" class="form-control" name="cantidad_alumnos" style="width:100px" placeholder="Ej: 30" min="1">
              <small class="text-danger error-message" id="error-cantidad_alumnos"></small>
            </td>
            <td>
              <input type="text" class="form-control" name="descripcion" style="width:100px" placeholder="Ej: Aula magna">
              <small class="text-danger error-message" id="error-descripcion"></small>
            </td>
            <td>
              <button class="btn btn-success btn-sm guardar-aula">Guardar</button>
              <button class="btn btn-secondary btn-sm cancelar-aula ml-1">Cancelar</button>
            </td>
          `;
          tabla.appendChild(nuevaFila);

          // Agregar validaciones en tiempo real
          const inputs = nuevaFila.querySelectorAll('input');
          inputs.forEach(input => {
            input.addEventListener('input', function() {
              validarCampoAula(this);
            });
            input.addEventListener('blur', function() {
              validarCampoAula(this);
            });
          });

          // Evento para cancelar
          nuevaFila.querySelector('.cancelar-aula').addEventListener('click', function() {
            nuevaFila.remove();
          });

          nuevaFila.querySelector('.guardar-aula').addEventListener('click', function () {
            const nro_aula = nuevaFila.querySelector('[name="nro_aula"]').value;
            const tamanio = nuevaFila.querySelector('[name="tamanio"]').value;
            const cantidad_alumnos = nuevaFila.querySelector('[name="cantidad_alumnos"]').value;
            const descripcion = nuevaFila.querySelector('[name="descripcion"]').value;

            // Validar todos los campos antes de enviar
            const esValido = validarTodosLosCamposAula(nuevaFila);
            if (!esValido) {
              return;
            }

            // Deshabilitar botón durante el envío
            this.disabled = true;
            this.textContent = 'Guardando...';

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
                // Mostrar mensaje de éxito con SweetAlert2
                Swal.fire({
                  icon: 'success',
                  title: 'Aula agregada correctamente',
                  text: 'El aula ha sido creada exitosamente.',
                  confirmButtonText: 'Entendido',
                  confirmButtonColor: '#28a745'
                }).then(() => {
                  // Recargar contenido y re-asignar eventos
                  cargarContenidoModal(institucionId);
                });
              } else {
                // Mostrar errores del servidor
                mostrarErroresServidor(nuevaFila, data.error);
                this.disabled = false;
                this.textContent = 'Guardar';
              }
            })
            .catch(error => {
              console.error('Error en fetch:', error);
              Swal.fire({
                icon: 'error',
                title: 'Error al guardar aula',
                text: 'Ocurrió un error al intentar guardar el aula. Por favor, intenta nuevamente.',
                confirmButtonText: 'Entendido',
                confirmButtonColor: '#d33'
              });
              this.disabled = false;
              this.textContent = 'Guardar';
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
      // Validar todos los campos antes de guardar
      const esValido = validarTodosLosCamposAula(fila);
      if (!esValido) {
        return;
      }

      // Guardar datos
      const nro_aula = fila.querySelector('[name="nro_aula"]').value;
      const tamanio = fila.querySelector('[name="tamanio"]').value;
      const cantidad = fila.querySelector('[name="cantidad_alumnos"]').value;
      const descripcion = fila.querySelector('[name="descripcion"]').value;
      const id = btn.getAttribute('data-id');

      // Deshabilitar botón durante el envío
      btn.disabled = true;
      btn.textContent = 'Guardando...';

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
          // Mostrar mensaje de éxito con SweetAlert2
          Swal.fire({
            icon: 'success',
            title: 'Aula modificada correctamente',
            text: 'Los cambios han sido guardados exitosamente.',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#28a745'
          }).then(() => {
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
          });
        } else {
          mostrarErroresServidor(fila, data.error);
          btn.disabled = false;
          btn.textContent = 'Guardar';
        }
      })
      .catch(error => {
        console.error('Error:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error al modificar aula',
          text: 'Ocurrió un error al intentar guardar los cambios. Por favor, intenta nuevamente.',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#d33'
        });
        btn.disabled = false;
        btn.textContent = 'Guardar';
      });
    } else {
      // Cambiar a modo edición
      const celdas = fila.querySelectorAll('td');
      const nro_aula = celdas[0].textContent.trim();
      const tamanio = celdas[1].textContent.trim();
      const cantidad = celdas[2].textContent.trim();
      const descripcion = celdas[3].textContent.trim();

      fila.innerHTML = `
        <td>
          <input class="form-control" type="text" name="nro_aula" value="${nro_aula}" />
          <small class="text-danger error-message" id="error-nro_aula"></small>
        </td>
        <td>
          <input class="form-control" type="number" name="tamanio" value="${tamanio}" min="1" />
          <small class="text-danger error-message" id="error-tamanio"></small>
        </td>
        <td>
          <input class="form-control" type="number" name="cantidad_alumnos" value="${cantidad}" min="1" />
          <small class="text-danger error-message" id="error-cantidad_alumnos"></small>
        </td>
        <td>
          <input class="form-control" type="text" name="descripcion" value="${descripcion}" />
          <small class="text-danger error-message" id="error-descripcion"></small>
        </td>
        <td>
          <button class="btn btn-success btn-sm modificar-aula" data-id="${btn.getAttribute('data-id')}">Guardar</button>
          <button class="btn btn-secondary btn-sm cancelar-edicion ml-1">Cancelar</button>
        </td>`;

      // Agregar validaciones en tiempo real para los campos de edición
      const inputs = fila.querySelectorAll('input');
      inputs.forEach(input => {
        input.addEventListener('input', function() {
          validarCampoAula(this);
        });
        input.addEventListener('blur', function() {
          validarCampoAula(this);
        });
      });

      // Evento para cancelar edición
      fila.querySelector('.cancelar-edicion').addEventListener('click', function() {
        fila.innerHTML = `
          <td>${nro_aula}</td>
          <td>${tamanio}</td>
          <td>${cantidad}</td>
          <td>${descripcion}</td>
          <td>
            <button class="btn btn-primary btn-sm modificar-aula" data-id="${btn.getAttribute('data-id')}">Modificar</button>
            <button class="btn btn-danger btn-sm eliminar-aula" data-id="${btn.getAttribute('data-id')}">Eliminar</button>
          </td>`;
        asignarEventosModificar();
        asignarEventosEliminar();
      });

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
    const fila = btn.closest('tr');
    const nroAula = fila.querySelector('td:first-child').textContent.trim();

    // Confirmación con SweetAlert2
    Swal.fire({
      title: '¿Confirmar eliminación?',
      html: `¿Estás seguro de que quieres eliminar el aula <strong>${nroAula}</strong>?<br><br>Esta acción no se puede deshacer.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        // Deshabilitar botón durante la eliminación
        btn.disabled = true;
        btn.textContent = 'Eliminando...';

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
            Swal.fire({
              icon: 'success',
              title: 'Aula eliminada correctamente',
              text: `El aula ${nroAula} ha sido eliminada exitosamente.`,
              confirmButtonText: 'Entendido',
              confirmButtonColor: '#28a745'
            }).then(() => {
              const institucionId = modalAulas.getAttribute('data-institucion-id');
              cargarContenidoModal(institucionId);
            });
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Error al eliminar aula',
              text: 'No se pudo eliminar el aula. Por favor, intenta nuevamente.',
              confirmButtonText: 'Entendido',
              confirmButtonColor: '#d33'
            });
            btn.disabled = false;
            btn.textContent = 'Eliminar';
          }
        })
        .catch(error => {
          console.error('Error eliminando aula:', error);
          Swal.fire({
            icon: 'error',
            title: 'Error inesperado',
            text: 'Ocurrió un error al intentar eliminar el aula. Por favor, intenta nuevamente.',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#d33'
          });
          btn.disabled = false;
          btn.textContent = 'Eliminar';
        });
      }
    });
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

// Funciones de validación para aulas
function validarCampoAula(input) {
  const nombre = input.name;
  const valor = input.value.trim();
  const errorElement = input.parentElement.querySelector(`#error-${nombre}`);
  
  let esValido = true;
  let mensaje = '';

  switch (nombre) {
    case 'nro_aula':
      if (valor.length < 1) {
        esValido = false;
        mensaje = 'El número de aula debe tener al menos 1 carácter.';
      } else if (valor.length > 10) {
        esValido = false;
        mensaje = 'El número de aula debe tener como máximo 10 caracteres.';
      } else if (!/^[a-zA-Z0-9\s]+$/.test(valor)) {
        esValido = false;
        mensaje = 'Numero invalido.';
      }
      break;

    case 'tamanio':
      const tamano = parseInt(valor);
      if (valor === '' || isNaN(tamano) || tamano <= 0) {
        esValido = false;
        mensaje = 'Tamaño invalido.';
      }
      break;

    case 'cantidad_alumnos':
      const cantidad = parseInt(valor);
      if (valor === '' || isNaN(cantidad) || cantidad <= 0) {
        esValido = false;
        mensaje = 'Cantidad invalida.';
      }
      break;

    case 'descripcion':
      if (valor.length > 100) {
        esValido = false;
        mensaje = 'La descripción del aula no puede exceder los 100 caracteres.';
      } else if (valor && !/^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$/.test(valor)) {
        esValido = false;
        mensaje = 'Descripción inválida';
      }
      break;
  }

  if (errorElement) {
    errorElement.textContent = mensaje;
    errorElement.style.display = mensaje ? 'block' : 'none';
  }

  // Cambiar el estilo del input según la validación
  if (esValido) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
  } else {
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');
  }

  return esValido;
}

function validarTodosLosCamposAula(fila) {
  const inputs = fila.querySelectorAll('input');
  let todoValido = true;

  inputs.forEach(input => {
    if (!validarCampoAula(input)) {
      todoValido = false;
    }
  });

  return todoValido;
}

function mostrarErroresServidor(fila, errores) {
  // Limpiar errores previos
  fila.querySelectorAll('.error-message').forEach(error => {
    error.textContent = '';
    error.style.display = 'none';
  });

  // Limpiar errores generales previos
  const errorGeneral = fila.querySelector('.error-general');
  if (errorGeneral) {
    errorGeneral.remove();
  }

  // Mostrar errores específicos
  if (Array.isArray(errores)) {
    // Si es un array de errores, mostrar el primer error en SweetAlert2
    if (errores.length > 0) {
      Swal.fire({
        icon: 'error',
        title: 'Error en los datos',
        html: `Se encontraron los siguientes errores:<br><ul>${errores.map(error => `<li>${error}</li>`).join('')}</ul>`,
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#d33'
      });
    }
  } else if (typeof errores === 'object') {
    // Si es un objeto con errores específicos por campo
    let hayErrores = false;
    Object.keys(errores).forEach(campo => {
      const errorElement = fila.querySelector(`#error-${campo}`);
      if (errorElement) {
        errorElement.textContent = errores[campo];
        errorElement.style.display = 'block';
        hayErrores = true;
      }
    });
    
    // Si hay errores de campos específicos, mostrar también un mensaje general
    if (hayErrores) {
      Swal.fire({
        icon: 'error',
        title: 'Errores en el formulario',
        text: 'Por favor, revisa los campos marcados en rojo y corrige los errores.',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#d33'
      });
    }
  } else {
    // Error general como string
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: errores,
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#d33'
    });
  }
}

function mostrarMensajeError(fila, mensaje) {
  // Mostrar error con SweetAlert2 en lugar de crear elementos DOM
  Swal.fire({
    icon: 'error',
    title: 'Error',
    text: mensaje,
    confirmButtonText: 'Entendido',
    confirmButtonColor: '#d33'
  });
}