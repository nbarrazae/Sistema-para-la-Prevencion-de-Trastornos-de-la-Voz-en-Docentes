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
            : `Aula ${item.nro_aula}`;
        
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
  
    modal.addEventListener('hidden.bs.modal', () => {
      institucionSelect.selectedIndex = 0;
      destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
      tipoDestinoInput.value = '';
      macInput.value = '';
      tipoDestino = ''; // Reset también
    });
  });
  