  document.addEventListener('DOMContentLoaded', () => {
    const asignarModal = document.getElementById('asignarDispositivoModal');
    const institucionSelect = document.getElementById('institucionSelect');
    const tipoDestino = document.getElementById('tipoDestino');
    const destinoSelect = document.getElementById('destinoSelect');
    const macInput = document.getElementById('macDispositivoSeleccionado');

    // Al abrir el modal, guardar la MAC
    asignarModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const mac = button.getAttribute('data-dispositivo');
      macInput.value = mac;
    });

    async function fetchOpciones() {
      const institucionId = institucionSelect.value;
      const tipo = tipoDestino.value;

      if (!institucionId || !tipo) {
        destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
        return;
      }

      const response = await fetch(`/obtener_opciones/${institucionId}/${tipo}/`);
      const data = await response.json();

      destinoSelect.innerHTML = '<option value="">Seleccione una opción</option>';
      data.forEach(item => {
        destinoSelect.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
      });
    }

    institucionSelect.addEventListener('change', fetchOpciones);
    tipoDestino.addEventListener('change', fetchOpciones);
  });
