// validatorDispositivo.js
// Valida el formato y unicidad de la MAC antes de enviar el formulario de agregar dispositivo IoT

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalAgregarDispositivo');
  if (!modal) return;
  const form = modal.querySelector('form');
  const macInput = form.querySelector('#mac_dispositivo');
  const macError = form.querySelector('#mac-error');
  const macRegex = /^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$/;

  // Validación en tiempo real
  macInput.addEventListener('input', function () {
    const macValue = macInput.value.trim();
    if (!macRegex.test(macValue)) {
      macError.textContent = 'Formato de MAC inválido. Ejemplo: 00:1A:2B:3C:4D:5E';
      macInput.classList.add('is-invalid');
    } else {
      macError.textContent = '';
      macInput.classList.remove('is-invalid');
    }
  });

  form.addEventListener('submit', async function(event) {
    const macValue = macInput.value.trim();

    if (!macRegex.test(macValue)) {
      event.preventDefault();
      macError.textContent = 'Formato de MAC inválido. Ejemplo: 00:1A:2B:3C:4D:5E';
      macInput.classList.add('is-invalid');
      Swal.fire({
        icon: 'error',
        title: 'Formato de MAC inválido',
        text: 'Ejemplo válido: 00:1A:2B:3C:4D:5E',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#d33'
      });
      return;
    } else {
      macError.textContent = '';
      macInput.classList.remove('is-invalid');
    }

    // Validación de MAC duplicada
    event.preventDefault();
    try {
      const existeResponse = await fetch(`/api/dispositivo_existe/${encodeURIComponent(macValue)}/`);
      if (existeResponse.ok) {
        const existeData = await existeResponse.json();
        if (existeData.existe) {
          macError.textContent = 'Ya existe un dispositivo con esa MAC.';
          macInput.classList.add('is-invalid');
          Swal.fire({
            icon: 'error',
            title: 'MAC duplicada',
            text: 'Ya existe un dispositivo con esa MAC.',
            confirmButtonText: 'Entendido',
            confirmButtonColor: '#d33'
          });
          return;
        }
      }
    } catch (error) {
      console.warn('No se pudo validar la MAC en el backend.');
    }

    // Enviar el formulario si todo está OK
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
          title: 'Dispositivo creado correctamente',
          text: 'El dispositivo ha sido agregado con éxito.',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#28a745'
        }).then(() => {
          location.reload();
        });
      } else {
        const data = await response.json();
        Swal.fire({
          icon: 'error',
          title: 'Error al crear el dispositivo',
          html: `No se pudo crear el dispositivo. Detalles:<br><ul>${Object.values(data).map(error => `<li>${error}</li>`).join('')}</ul>`,
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#d33'
        });
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error inesperado',
        text: 'Ocurrió un error al intentar crear el dispositivo.',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#d33'
      });
    }
  });
});
