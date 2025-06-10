document.getElementById('institucion').addEventListener('change', async function () {
  const idInstitucion = this.value;
  const profesorSelect = document.getElementById('profesor');
  profesorSelect.innerHTML = '<option value="">Cargando...</option>';

  try {
    const response = await fetch(`/api/profesores_por_institucion/${idInstitucion}/`);
    const datos = await response.json();

    profesorSelect.innerHTML = '<option value="">Seleccione un profesor</option>';
    datos.forEach(item => {
      const nombre = `${item.nombre_profesor} ${item.apellido_profesor}`;
      profesorSelect.innerHTML += `<option value="${item.id_profesor}">${nombre}</option>`;
    });
  } catch (error) {
    profesorSelect.innerHTML = '<option value="">Error al cargar profesores</option>';
    console.error(error);
  }
});
