document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalHorarioProfesor');
  
    modal.addEventListener('show.bs.modal', async function (event) {
      const button = event.relatedTarget;
  
      const profesorId = button.getAttribute('data-id');
      const nombre = button.getAttribute('data-nombre');
      const institucionId = button.getAttribute('data-institucion');
  
      document.getElementById('idProfesorHorario').value = profesorId;
      document.getElementById('nombreProfesorHorario').textContent = nombre;
  
      // Cargar aulas según institución (AJAX)
      const aulaSelect = document.getElementById('selectAulas');
      aulaSelect.innerHTML = '<option value="">Cargando aulas...</option>';
      const aulas = await fetch(`/aulas_por_institucion/${institucionId}/`).then(r => r.json());
  
      aulaSelect.innerHTML = '<option value="">Selecciona un aula</option>';
      aulas.forEach(aula => {
        const option = document.createElement('option');
        option.value = aula.id_aula;
        option.textContent = aula.nro_aula;
        aulaSelect.appendChild(option);
      });
  
      // Cargar horarios actuales del profesor (AJAX)
      const horariosDiv = document.getElementById('listaHorariosProfesor');
      horariosDiv.innerHTML = 'Cargando horarios...';
  
      const horarios = await fetch(`/horarios_por_profesor/${profesorId}/`).then(r => r.json());
  
      horariosDiv.innerHTML = horarios.map(h => `
        <div class="border p-2 mb-2 d-flex justify-content-between align-items-center">
          <span>${h.dia}: ${h.hora_inicio} - ${h.hora_termino} | Aula: ${h.nombre_aula}</span>
          <button class="btn btn-sm btn-danger" onclick="eliminarHorario(${h.id_horario})">Eliminar</button>
        </div>
      `).join('');
    });
  });
  

  document.getElementById('formHorarioProfesor').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevenir recarga
  
    const id_profesor = document.getElementById('idProfesorHorario').value;
    const dia = this.dia.value;
    const hora_inicio = this.hora_inicio.value;
    const hora_termino = this.hora_termino.value;
    const id_aula = this.id_aula.value;
  
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    const response = await fetch('/agregar_horario/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ id_profesor, dia, hora_inicio, hora_termino, id_aula })
    });
  
    const result = await response.json();
  
    if (result.success) {
      alert('Horario agregado correctamente');
  
      // Refresca la lista de horarios
      const horarios = await fetch(`/horarios_por_profesor/${id_profesor}/`).then(r => r.json());
      const horariosDiv = document.getElementById('listaHorariosProfesor');
      horariosDiv.innerHTML = horarios.map(h => `
        <div class="border p-2 mb-2 d-flex justify-content-between align-items-center">
          <span>${h.dia}: ${h.hora_inicio} - ${h.hora_termino} | Aula: ${h.nombre_aula}</span>
          <button class="btn btn-sm btn-danger" onclick="eliminarHorario(${h.id_horario})">Eliminar</button>
        </div>
      `).join('');
      
  
      // Limpia el formulario (opcional)
      this.reset();
    } else {
      alert('Error al agregar horario');
    }
  });


async function eliminarHorario(idHorario) {
    if (!confirm('¿Eliminar este horario?')) return;
  
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    const response = await fetch(`/eliminar_horario/${idHorario}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      }
    });
  
    const result = await response.json();
  
    if (result.success) {
    //   alert('Horario eliminado correctamente');
  
      // Recarga la lista actualizada de horarios
      const id_profesor = document.getElementById('idProfesorHorario').value;
      const horarios = await fetch(`/horarios_por_profesor/${id_profesor}/`).then(r => r.json());
      const horariosDiv = document.getElementById('listaHorariosProfesor');
      horariosDiv.innerHTML = horarios.map(h => `
        <div class="border p-2 mb-2 d-flex justify-content-between align-items-center">
          <span>${h.dia}: ${h.hora_inicio} - ${h.hora_termino} | Aula: ${h.nombre_aula}</span>
          <button class="btn btn-sm btn-danger" onclick="eliminarHorario(${h.id_horario})">Eliminar</button>
        </div>
      `).join('');
    } else {
      alert('Error al eliminar el horario');
    }
  }
  