// Funciones para consultas personalizadas

// Configuración de campos por tabla
const camposTablas = {
  predicadores: ['id', 'Nombre', 'Apellido', 'Numero', 'estado', 'fecha'],
  bandeja: ['id', 'Objetivo', 'Descripcion', 'estado', 'fecha'],
  reuniones: ['id', 'Dirige', 'Lectura', 'Cantos_alegre', 'Ofrenda', 'Predica', 'estado', 'fecha'],
  finanzas: ['id', 'Concepto', 'Monto', 'Fecha', 'Observaciones', 'estado', 'fecha'],
  asistencias: ['id', 'Nombre', 'Numero', 'unoviernes', 'dosviernes', 'tresViernes', 'cuatroviernes', 'cincoviernes', 'estado', 'fecha'],
  jovenes: ['id', 'Nombre', 'Apellido', 'Numero', 'estado', 'fecha'],
  calendario: ['id', 'Evento', 'Fecha', 'Observaciones', 'estado', 'fecha']
};

// Función para cargar campos cuando se selecciona una tabla
function cargarCampos() {
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const camposDisponibles = document.getElementById('camposDisponibles');
  
  if (!tablaSeleccionada) {
    camposDisponibles.innerHTML = '<p>Seleccione una tabla para ver los campos disponibles</p>';
    return;
  }
  
  const campos = camposTablas[tablaSeleccionada] || [];
  let html = '';
  
  campos.forEach(campo => {
    html += `
      <div class="campo-checkbox">
        <input type="checkbox" id="campo_${campo}" value="${campo}" checked>
        <label for="campo_${campo}">${campo}</label>
      </div>
    `;
  });
  
  camposDisponibles.innerHTML = html;
  
  // Actualizar campos en condiciones WHERE y ordenamiento
  actualizarCamposWhere();
  actualizarCamposOrden();
}

// Función para actualizar campos en condiciones WHERE
function actualizarCamposWhere() {
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const campos = camposTablas[tablaSeleccionada] || [];
  const selectsWhere = document.querySelectorAll('.campo-where');
  
  selectsWhere.forEach(select => {
    const valorActual = select.value;
    select.innerHTML = '<option value="">Seleccionar campo</option>';
    
    campos.forEach(campo => {
      const option = document.createElement('option');
      option.value = campo;
      option.textContent = campo;
      select.appendChild(option);
    });
    
    // Restaurar valor anterior si existe
    if (valorActual && campos.includes(valorActual)) {
      select.value = valorActual;
    }
  });
}

// Función para actualizar campos en ordenamiento
function actualizarCamposOrden() {
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const campos = camposTablas[tablaSeleccionada] || [];
  const selectsOrden = document.querySelectorAll('.campo-orden');
  
  selectsOrden.forEach(select => {
    const valorActual = select.value;
    select.innerHTML = '<option value="">Seleccionar campo</option>';
    
    campos.forEach(campo => {
      const option = document.createElement('option');
      option.value = campo;
      option.textContent = campo;
      select.appendChild(option);
    });
    
    // Restaurar valor anterior si existe
    if (valorActual && campos.includes(valorActual)) {
      select.value = valorActual;
    }
  });
}

// Función para agregar condición WHERE
function agregarCondicion() {
  const contenedor = document.getElementById('condicionesWhere');
  const nuevaCondicion = document.createElement('div');
  nuevaCondicion.className = 'condicion-fila';
  
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const campos = camposTablas[tablaSeleccionada] || [];
  
  let camposOptions = '<option value="">Seleccionar campo</option>';
  campos.forEach(campo => {
    camposOptions += `<option value="${campo}">${campo}</option>`;
  });
  
  nuevaCondicion.innerHTML = `
    <select class="campo-where">
      ${camposOptions}
    </select>
    <select class="operador-where">
      <option value="=">=</option>
      <option value="!=">!=</option>
      <option value=">">></option>
      <option value="<"><</option>
      <option value=">=">>=</option>
      <option value="<="><=</option>
      <option value="LIKE">LIKE</option>
      <option value="IN">IN</option>
    </select>
    <input type="text" class="valor-where" placeholder="Valor">
    <button type="button" class="btn btn-danger btn-sm" onclick="eliminarCondicion(this)">Eliminar</button>
  `;
  
  contenedor.appendChild(nuevaCondicion);
}

// Función para eliminar condición WHERE
function eliminarCondicion(boton) {
  const condicion = boton.closest('.condicion-fila');
  if (condicion) {
    condicion.remove();
  }
}

// Función para agregar orden
function agregarOrden() {
  const contenedor = document.getElementById('ordenamiento');
  const nuevoOrden = document.createElement('div');
  nuevoOrden.className = 'orden-fila';
  
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const campos = camposTablas[tablaSeleccionada] || [];
  
  let camposOptions = '<option value="">Seleccionar campo</option>';
  campos.forEach(campo => {
    camposOptions += `<option value="${campo}">${campo}</option>`;
  });
  
  nuevoOrden.innerHTML = `
    <select class="campo-orden">
      ${camposOptions}
    </select>
    <select class="tipo-orden">
      <option value="ASC">Ascendente</option>
      <option value="DESC">Descendente</option>
    </select>
    <button type="button" class="btn btn-danger btn-sm" onclick="eliminarOrden(this)">Eliminar</button>
  `;
  
  contenedor.appendChild(nuevoOrden);
}

// Función para eliminar orden
function eliminarOrden(boton) {
  const orden = boton.closest('.orden-fila');
  if (orden) {
    orden.remove();
  }
}

// Función para generar SQL
function generarSQL() {
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const limite = document.getElementById('limiteResultados').value;
  
  if (!tablaSeleccionada) {
    return '-- Seleccione una tabla para generar SQL';
  }
  
  // Obtener campos seleccionados
  const camposSeleccionados = [];
  document.querySelectorAll('#camposDisponibles input[type="checkbox"]:checked').forEach(checkbox => {
    camposSeleccionados.push(checkbox.value);
  });
  
  if (camposSeleccionados.length === 0) {
    return '-- Seleccione al menos un campo';
  }
  
  // Construir SELECT
  let sql = `SELECT ${camposSeleccionados.join(', ')}\nFROM ${tablaSeleccionada}`;
  
  // Construir WHERE
  const condiciones = [];
  document.querySelectorAll('.condicion-fila').forEach(fila => {
    const campo = fila.querySelector('.campo-where').value;
    const operador = fila.querySelector('.operador-where').value;
    const valor = fila.querySelector('.valor-where').value;
    
    if (campo && operador && valor) {
      if (operador === 'LIKE') {
        condiciones.push(`${campo} LIKE '%${valor}%'`);
      } else if (operador === 'IN') {
        const valores = valor.split(',').map(v => `'${v.trim()}'`).join(', ');
        condiciones.push(`${campo} IN (${valores})`);
      } else {
        condiciones.push(`${campo} ${operador} '${valor}'`);
      }
    }
  });
  
  if (condiciones.length > 0) {
    sql += `\nWHERE ${condiciones.join(' AND ')}`;
  }
  
  // Construir ORDER BY
  const ordenes = [];
  document.querySelectorAll('.orden-fila').forEach(fila => {
    const campo = fila.querySelector('.campo-orden').value;
    const tipo = fila.querySelector('.tipo-orden').value;
    
    if (campo && tipo) {
      ordenes.push(`${campo} ${tipo}`);
    }
  });
  
  if (ordenes.length > 0) {
    sql += `\nORDER BY ${ordenes.join(', ')}`;
  }
  
  // Agregar LIMIT
  if (limite && limite > 0) {
    sql += `\nLIMIT ${limite}`;
  }
  
  return sql;
}

// Función para ejecutar consulta
async function ejecutarConsulta() {
  if (!checkAuthentication()) return;
  
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  if (!tablaSeleccionada) {
    alert('Seleccione una tabla para ejecutar la consulta');
    return;
  }
  
  // Generar SQL
  const sql = generarSQL();
  document.getElementById('sqlGenerado').textContent = sql;
  
  // Mostrar loading
  const resultadosConsulta = document.getElementById('resultadosConsulta');
  resultadosConsulta.innerHTML = '<div class="cargando-consulta"><div class="spinner"></div><p>Ejecutando consulta...</p></div>';
  
  try {
    const response = await fetch('/api/consultas/ejecutar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tabla: tablaSeleccionada,
        sql: sql
      })
    });

    const resultado = await response.json();
    
    if (resultado.success) {
      mostrarResultadosConsulta(resultado.data);
    } else {
      resultadosConsulta.innerHTML = `<div class="error-consulta">Error: ${resultado.mensaje}</div>`;
    }
  } catch (error) {
    console.error('Error al ejecutar consulta:', error);
    resultadosConsulta.innerHTML = '<div class="error-consulta">Error al ejecutar la consulta</div>';
  }
}

// Función para mostrar resultados de la consulta
function mostrarResultadosConsulta(datos) {
  const resultadosConsulta = document.getElementById('resultadosConsulta');
  
  if (!datos || datos.length === 0) {
    resultadosConsulta.innerHTML = '<p class="mensaje-inicial">No se encontraron resultados</p>';
    return;
  }
  
  // Obtener campos de la primera fila
  const campos = Object.keys(datos[0]);
  
  let html = '<table class="tabla-consulta">';
  
  // Encabezados
  html += '<thead><tr>';
  campos.forEach(campo => {
    html += `<th>${campo}</th>`;
  });
  html += '</tr></thead>';
  
  // Datos
  html += '<tbody>';
  datos.forEach(fila => {
    html += '<tr>';
    campos.forEach(campo => {
      const valor = fila[campo] || '';
      html += `<td>${valor}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody>';
  
  html += '</table>';
  
  // Agregar estadísticas
  html += `
    <div class="estadisticas-consulta">
      <div class="estadistica-item">
        <div class="numero">${datos.length}</div>
        <div class="etiqueta">Registros</div>
      </div>
      <div class="estadistica-item">
        <div class="numero">${campos.length}</div>
        <div class="etiqueta">Campos</div>
      </div>
    </div>
  `;
  
  resultadosConsulta.innerHTML = html;
}

// Función para limpiar consulta
function limpiarConsulta() {
  document.getElementById('tablaSeleccionada').value = '';
  document.getElementById('camposDisponibles').innerHTML = '<p>Seleccione una tabla para ver los campos disponibles</p>';
  document.getElementById('condicionesWhere').innerHTML = `
    <div class="condicion-fila">
      <select class="campo-where">
        <option value="">Seleccionar campo</option>
      </select>
      <select class="operador-where">
        <option value="=">=</option>
        <option value="!=">!=</option>
        <option value=">">></option>
        <option value="<"><</option>
        <option value=">=">>=</option>
        <option value="<="><=</option>
        <option value="LIKE">LIKE</option>
        <option value="IN">IN</option>
      </select>
      <input type="text" class="valor-where" placeholder="Valor">
      <button type="button" class="btn btn-danger btn-sm" onclick="eliminarCondicion(this)">Eliminar</button>
    </div>
  `;
  document.getElementById('ordenamiento').innerHTML = `
    <div class="orden-fila">
      <select class="campo-orden">
        <option value="">Seleccionar campo</option>
      </select>
      <select class="tipo-orden">
        <option value="ASC">Ascendente</option>
        <option value="DESC">Descendente</option>
      </select>
      <button type="button" class="btn btn-danger btn-sm" onclick="eliminarOrden(this)">Eliminar</button>
    </div>
  `;
  document.getElementById('limiteResultados').value = '100';
  document.getElementById('resultadosConsulta').innerHTML = '<p class="mensaje-inicial">Ejecute una consulta para ver los resultados</p>';
  document.getElementById('sqlGenerado').textContent = '-- El SQL se generará automáticamente';
}

// Función para guardar consulta
async function guardarConsulta() {
  if (!checkAuthentication()) return;
  
  const nombre = prompt('Ingrese un nombre para la consulta:');
  if (!nombre) return;
  
  const descripcion = prompt('Ingrese una descripción (opcional):');
  
  const consulta = {
    nombre: nombre,
    descripcion: descripcion || '',
    tabla: document.getElementById('tablaSeleccionada').value,
    sql: generarSQL(),
    fecha: new Date().toISOString()
  };
  
  try {
    const response = await fetch('/api/consultas/guardar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(consulta)
    });

    const resultado = await response.json();
    
    if (resultado.success) {
      alert('Consulta guardada exitosamente');
      cargarConsultasGuardadas();
    } else {
      alert('Error al guardar la consulta: ' + resultado.mensaje);
    }
  } catch (error) {
    console.error('Error al guardar consulta:', error);
    alert('Error al guardar la consulta');
  }
}

// Función para cargar consultas guardadas
async function cargarConsultasGuardadas() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/consultas/guardadas');
    const resultado = await response.json();
    
    const listaConsultas = document.getElementById('listaConsultasGuardadas');
    
    if (resultado.success && resultado.data && resultado.data.length > 0) {
      let html = '';
      resultado.data.forEach(consulta => {
        html += `
          <div class="consulta-guardada" onclick="cargarConsulta('${consulta.id}')">
            <div class="nombre">${consulta.nombre}</div>
            <div class="descripcion">${consulta.descripcion}</div>
            <div class="acciones">
              <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); ejecutarConsultaGuardada('${consulta.id}')">Ejecutar</button>
              <button class="btn btn-danger btn-sm" onclick="event.stopPropagation(); eliminarConsultaGuardada('${consulta.id}')">Eliminar</button>
            </div>
          </div>
        `;
      });
      listaConsultas.innerHTML = html;
    } else {
      listaConsultas.innerHTML = '<p>No hay consultas guardadas</p>';
    }
  } catch (error) {
    console.error('Error al cargar consultas guardadas:', error);
  }
}

// Función para exportar resultados
async function exportarResultados() {
  if (!checkAuthentication()) return;
  
  const formato = document.querySelector('input[name="formato"]:checked').value;
  const tablaSeleccionada = document.getElementById('tablaSeleccionada').value;
  const sql = generarSQL();
  
  if (!tablaSeleccionada) {
    alert('Seleccione una tabla para exportar');
    return;
  }
  
  try {
    const response = await fetch('/api/consultas/exportar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tabla: tablaSeleccionada,
        sql: sql,
        formato: formato
      })
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `consulta_${tablaSeleccionada}_${new Date().toISOString().split('T')[0]}.${formato}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } else {
      alert('Error al exportar los resultados');
    }
  } catch (error) {
    console.error('Error al exportar:', error);
    alert('Error al exportar los resultados');
  }
}

// Función para copiar SQL
function copiarSQL() {
  const sql = document.getElementById('sqlGenerado').textContent;
  navigator.clipboard.writeText(sql).then(() => {
    alert('SQL copiado al portapapeles');
  }).catch(() => {
    alert('Error al copiar SQL');
  });
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  cargarConsultasGuardadas();
  
  // Actualizar SQL cuando cambien los campos
  document.addEventListener('change', function() {
    if (document.getElementById('tablaSeleccionada').value) {
      document.getElementById('sqlGenerado').textContent = generarSQL();
    }
  });
});
