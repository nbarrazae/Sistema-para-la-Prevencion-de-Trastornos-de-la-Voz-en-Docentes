document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('asignarDispositivoModal');
    const macInput = document.getElementById('macDispositivoSeleccionado');
    const tipoDestinoInput = document.getElementById('tipoDestino');
    const institucionSelect = document.getElementById('institucionSelect');
    const destinoSelect = document.getElementById('destinoSelect');
  
    let tipoDestino = ''; // Variable global para saber si cargar profesores o aulas
  
    // Escucha solo UNA VEZ cuando cambia la institución
    institucionSelect.addEventListener('change', async () => {
      const idInstitucion = institucionSelect.value;
      if (!idInstitucion || !tipoDestino) return;
  
      let url = tipoDestino === 'profesor'
        ? `/api/profesores_por_institucion/${idInstitucion}/`
        : `/api/aulas_por_institucion/${idInstitucion}/`;
  
      try {
        const response = await fetch(url);
        const datos = await response.json();
  
        destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
        datos.forEach(item => {
          const nombre = tipoDestino === 'profesor'
            ? `${item.nombre_profesor} ${item.apellido_profesor}`
            : `${item.nro_aula}`;
        
          const id = tipoDestino === 'profesor'
            ? item.id_profesor
            : item.id_aula;
        
          destinoSelect.innerHTML += `<option value="${id}">${nombre}</option>`;
        });
        
      } catch (error) {
        destinoSelect.innerHTML = '<option value="">Error al cargar</option>';
        console.error(error);
      }
    });
  
    // Solo define los datos cuando se abre el modal
    modal.addEventListener('show.bs.modal', async event => {
      const button = event.relatedTarget;
      const mac = button.getAttribute('data-mac');
      const tipo = button.getAttribute('data-tipo');
  
      macInput.value = mac;
  
      const tipoNormalizado = tipo.toLowerCase();
  
      if (tipoNormalizado.includes('dosímetro')) {
        tipoDestino = 'profesor';
      } else if (tipoNormalizado.includes('registrador')) {
        tipoDestino = 'aula';
      } else {
        tipoDestino = '';
      }
  
      tipoDestinoInput.value = tipoDestino;
  
      // Resetear campos visibles
      institucionSelect.selectedIndex = 0;
      destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
    });
  
    // Al enviar el formulario de asignación
    const form = modal.querySelector('form');
    form.addEventListener('submit', async function(event) {
      event.preventDefault();
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: {
            'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
          },
          body: new FormData(form)
        });
        if (response.ok) {
          Swal.fire({
            icon: 'success',
            title: 'Dispositivo asignado correctamente',
            text: 'El dispositivo ha sido asignado con éxito.',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#28a745'
          }).then(() => {
            location.reload();
          });
        } else {
          const data = await response.json();
          Swal.fire({
            icon: 'error',
            title: 'Error al asignar el dispositivo',
            html: `No se pudo asignar el dispositivo. Detalles:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#d33'
          });
        }
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error inesperado',
          text: 'Ocurrió un error al intentar asignar el dispositivo.',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#d33'
        });
      }
    });

    modal.addEventListener('hidden.bs.modal', () => {
      institucionSelect.selectedIndex = 0;
      destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
      tipoDestinoInput.value = '';
      macInput.value = '';
      tipoDestino = ''; // Reset también
    });
  });
  