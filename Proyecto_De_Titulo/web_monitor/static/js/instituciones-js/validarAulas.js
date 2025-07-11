document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formulario_aula');
  
    if (formulario) {
      formulario.addEventListener('submit', function (e) {
        e.preventDefault(); // Previene el envío si hay errores
  
        // Obtener valores de los inputs
        const nroAula = document.getElementById('nro_aula_input').value.trim();
        const tamano = document.getElementById('tamano_input').value.trim();
        const cantidad = document.getElementById('cantidad_alumnos_input').value.trim();
        const descripcion = document.getElementById('descripcion_input').value.trim();
  
        // Inicializar lista de errores
        let errores = [];
  
        // Validaciones
        if (!nroAula) {
          errores.push('El número de aula es obligatorio.');
        } else if (!/^[a-zA-Z0-9]+$/.test(nroAula)) {
          errores.push('El número de aula solo debe contener letras y números.');
        }
  
        if (!tamano) {
          errores.push('El tamaño es obligatorio.');
        } else if (isNaN(tamano) || parseInt(tamano) <= 0) {
          errores.push('El tamaño debe ser un número positivo.');
        }
  
        if (!cantidad) {
          errores.push('La cantidad de alumnos es obligatoria.');
        } else if (isNaN(cantidad) || parseInt(cantidad) <= 0) {
          errores.push('La cantidad de alumnos debe ser un número positivo.');
        }
  
        if (!descripcion) {
          errores.push('La descripción es obligatoria.');
        } else if (descripcion.length > 100) {
          errores.push('La descripción no debe superar los 100 caracteres.');
        }
  
        // Mostrar errores si existen
        if (errores.length > 0) {
          alert(errores.join('\n'));
          return;
        }
  
        // Si todo está bien, se puede proceder con la lógica de guardar
        // Aquí puedes llamar a una función que haga el fetch o submit real
        console.log('Validación pasada. Puedes guardar el aula.');
  
        // Si quieres enviar el formulario luego de validar manualmente, puedes descomentar esto:
        // formulario.submit();
      });
    }
  });