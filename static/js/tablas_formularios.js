// Funciones para Administradores
async function registrarAdmin(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  
  try {
    const response = await fetch('/api/admin/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    if (resultado.success) {
      alert("Administrador agregado exitosamente");
      limpiarAdmin();
      buscarAdmins();
    } else {
      alert("Error: " + resultado.mensaje);
    }
  } catch (error) {
    console.error('Error al registrar admin:', error);
    alert("Error al registrar administrador");
  }
}

async function buscarAdmins() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/admin/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaAdmins");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      tabla.innerHTML = '<div class="error-message">No se encontraron administradores</div>';
      return;
    }

    resultados.data.forEach((admin) => {
      const fecha = admin.fecha ? new Date(admin.fecha).toLocaleString() : 'N/A';
      const filaHtml = `
        <div>
          ${admin.email} | ${admin.nombre} | ${admin.rol} | ${fecha}
          <div class="button-group">
            <button class="btn btn-secondary" onclick="eliminarAdmin('${admin.email}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar admins:', error);
    alert("Error al buscar administradores");
  }
}

async function eliminarAdmin(email) {
  if (!checkAuthentication()) return;
  
  if (confirm("¿Está seguro que desea eliminar este administrador?")) {
    try {
      const response = await fetch(`/api/admin/eliminar/${email}`, {
        method: 'DELETE'
      });
      
      const resultado = await response.json();
      
      if (resultado.success) {
        alert("Administrador eliminado correctamente");
        buscarAdmins();
      } else {
        alert("Error: " + resultado.mensaje);
      }
    } catch (error) {
      console.error('Error al eliminar admin:', error);
      alert("Error al eliminar administrador");
    }
  }
}

function limpiarAdmin() {
  const form = document.querySelector("#formAdmins form");
  form.reset();
}

// Funciones para Predicadores
async function registrarPredicadores(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  
  // Asegurar que tenemos todos los campos necesarios
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  // Mostrar pantalla de carga
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/predicadores/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarPredicadores();
      buscarPredicadores();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarPredicadores() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/predicadores/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaPredicadores");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Predicadores', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const estadoDisplay = normalizarEstado(registro.estado);
      const filaHtml = `
        <div data-id="${registro.id}" class="registro-fila">
          <div class="registro-contenido">
            <strong>ID:</strong> ${registro.id || 'N/A'} | 
            <strong>Nombre:</strong> ${registro.Nombre || 'N/A'} | 
            <strong>Apellido:</strong> ${registro.Apellido || 'N/A'} | 
            <strong>Numero:</strong> ${registro.Numero || 'N/A'} | 
            <strong>Fecha:</strong> ${fechaFormateada} |
            <strong>Estado:</strong> ${estadoDisplay}
          </div>
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarPredicadores('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarPredicadores('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

async function mostrarEditarPredicadores(id) {
  const numericId = parseInt(id);
  if (isNaN(numericId)) {
    alert('ID inválido');
    return;
  }

  try {
    const response = await fetch(`/api/tablas/predicadores/buscar/${numericId}`);
    const resultado = await response.json();
    
    if (!resultado.success || !resultado.data) {
      alert('No se encontró el registro');
      return;
    }
    
    const datos = resultado.data;
    const modal = document.getElementById("modalEditarPredicadores");
    const form = document.getElementById("formEditarPredicadores");
    
    form.querySelector("[name='id']").value = datos.id;
    form.querySelector("[name='Nombre']").value = datos.Nombre;
    form.querySelector("[name='Apellido']").value = datos.Apellido;
    form.querySelector("[name='Numero']").value = datos.Numero;
    
    modal.style.display = 'block';
  } catch (error) {
    console.error('Error al buscar registro:', error);
    alert('Error al buscar el registro');
  }
}

function cerrarModalPredicadores() {
  document.getElementById('modalEditarPredicadores').style.display = 'none';
}

async function guardarEdicionPredicadores(event) {
  if (!checkAuthentication()) return;
  
  event.preventDefault();
  const form = event.target;
  const datos = Object.fromEntries(new FormData(form));
  datos.id = validarId(datos.id);
  datos.estado = 'Editado';
  
  // Mostrar pantalla de carga
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/predicadores/editar', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Editado correctamente");
      cerrarModalPredicadores();
      buscarPredicadores();
    } else {
      alert("Error al editar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    alert("Error: " + error.message);
  }
}

async function eliminarPredicadores(id) {
  if (!checkAuthentication()) return;
  
  if (confirm("¿Está seguro que desea eliminar este registro?")) {
    // Mostrar pantalla de carga
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    try {
      const response = await fetch(`/api/tablas/predicadores/eliminar/${id}`, {
        method: 'DELETE'
      });
      
      const resultado = await response.json();
      
      document.getElementById('loadingOverlay').style.display = 'none';
      
      if (resultado.success) {
        alert("Eliminado correctamente");
        limpiarPredicadores();
        buscarPredicadores();
      } else {
        alert("Error al eliminar: " + resultado.mensaje);
        buscarPredicadores();
      }
    } catch (error) {
      document.getElementById('loadingOverlay').style.display = 'none';
      console.error('Error al eliminar:', error);
      alert("Error al eliminar: " + error.message);
      buscarPredicadores();
    }
  }
}

function limpiarPredicadores() {
  const form = document.querySelector("#formPredicadores form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones para Bandeja
async function registrarBandeja(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  
  // Asegurar que tenemos todos los campos necesarios
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  // Mostrar pantalla de carga
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/bandeja/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarBandeja();
      buscarBandeja();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarBandeja() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/bandeja/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaBandeja");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Bandeja', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const estadoDisplay = normalizarEstado(registro.estado);
      const filaHtml = `
        <div data-id="${registro.id}" class="registro-fila">
          <div class="registro-contenido">
            <strong>ID:</strong> ${registro.id || 'N/A'} | 
            <strong>Objetivo:</strong> ${registro.Objetivo || 'N/A'} | 
            <strong>Descripción:</strong> ${registro.Descripcion || 'N/A'} | 
            <strong>Fecha:</strong> ${fechaFormateada} |
            <strong>Estado:</strong> ${estadoDisplay}
          </div>
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarBandeja('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarBandeja('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

async function mostrarEditarBandeja(id) {
  const numericId = parseInt(id);
  if (isNaN(numericId)) {
    alert('ID inválido');
    return;
  }

  try {
    const response = await fetch(`/api/tablas/bandeja/buscar/${numericId}`);
    const resultado = await response.json();
    
    if (!resultado.success || !resultado.data) {
      alert('No se encontró el registro');
      return;
    }
    
    const datos = resultado.data;
    const modal = document.getElementById("modalEditarBandeja");
    const form = document.getElementById("formEditarBandeja");
    
    form.querySelector("[name='id']").value = datos.id;
    form.querySelector("[name='Objetivo']").value = datos.Objetivo;
    form.querySelector("[name='Descripcion']").value = datos.Descripcion;
    
    modal.style.display = 'block';
  } catch (error) {
    console.error('Error al buscar registro:', error);
    alert('Error al buscar el registro');
  }
}

function cerrarModalBandeja() {
  document.getElementById('modalEditarBandeja').style.display = 'none';
}

async function guardarEdicionBandeja(event) {
  if (!checkAuthentication()) return;
  
  event.preventDefault();
  const form = event.target;
  const datos = Object.fromEntries(new FormData(form));
  datos.id = parseInt(datos.id);
  datos.estado = 'Editado';
  
  // Mostrar pantalla de carga
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/bandeja/editar', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Editado correctamente");
      cerrarModalBandeja();
      buscarBandeja();
    } else {
      alert("Error al editar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    alert("Error al editar: " + error.message);
  }
}

async function eliminarBandeja(id) {
  if (!checkAuthentication()) return;
  
  if (confirm("¿Está seguro que desea eliminar este registro?")) {
    // Mostrar pantalla de carga
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    try {
      const response = await fetch(`/api/tablas/bandeja/eliminar/${id}`, {
        method: 'DELETE'
      });
      
      const resultado = await response.json();
      
      document.getElementById('loadingOverlay').style.display = 'none';
      
      if (resultado.success) {
        alert("Eliminado correctamente");
        limpiarBandeja();
        buscarBandeja();
      } else {
        alert("Error al eliminar: " + resultado.mensaje);
        buscarBandeja();
      }
    } catch (error) {
      document.getElementById('loadingOverlay').style.display = 'none';
      console.error('Error al eliminar:', error);
      alert("Error al eliminar: " + error.message);
      buscarBandeja();
    }
  }
}

function limpiarBandeja() {
  const form = document.querySelector("#formBandeja form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones similares para las demás tablas (Asistencias, Jóvenes, Finanzas, Calendario, Reuniones)
// Se implementan con el mismo patrón pero adaptadas a cada tabla específica

// Funciones para Asistencias
async function registrarAsistencias(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/asistencias/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarAsistencias();
      buscarAsistencias();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarAsistencias() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/asistencias/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaAsistencias");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Asistencias', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const filaHtml = `
        <div data-id="${registro.id}">
          ${registro.id} | ${registro.Nombre} | ${registro.Numero} | ${registro.unoviernes} | ${registro.dosviernes} | ${registro.tresViernes} | ${registro.cuatroviernes} | ${registro.cincoviernes} | ${fechaFormateada}
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarAsistencias('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarAsistencias('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

// Funciones similares para las demás tablas...
// Por simplicidad, aquí solo se muestran las funciones principales
// Las funciones completas seguirían el mismo patrón para cada tabla

function limpiarAsistencias() {
  const form = document.querySelector("#formAsistencias form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones para Jóvenes
async function registrarJovenes(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/jovenes/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarJovenes();
      buscarJovenes();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarJovenes() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/jovenes/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaJovenes");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Jovenes', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const filaHtml = `
        <div data-id="${registro.id}">
          ${registro.id} | ${registro.Nombre} | ${registro.Apellido} | ${registro.Numero} | ${fechaFormateada}
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarJovenes('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarJovenes('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

function limpiarJovenes() {
  const form = document.querySelector("#formJovenes form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones para Finanzas
async function registrarFinanzas(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/finanzas/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarFinanzas();
      buscarFinanzas();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarFinanzas() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/finanzas/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaFinanzas");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Finanzas', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const filaHtml = `
        <div data-id="${registro.id}">
          ${registro.id} | ${registro.Concepto} | ${registro.Monto} | ${registro.Fecha} | ${registro.Observaciones} | ${fechaFormateada}
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarFinanzas('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarFinanzas('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

function limpiarFinanzas() {
  const form = document.querySelector("#formFinanzas form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones para Calendario
async function registrarCalendario(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/calendario/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarCalendario();
      buscarCalendario();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarCalendario() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/calendario/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaCalendario");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Calendario', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.Fecha_de_Registro);
      const filaHtml = `
        <div data-id="${registro.id}">
          ${registro.id} | ${registro.Evento} | ${registro.Fecha} | ${registro.Observaciones} | ${fechaFormateada}
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarCalendario('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarCalendario('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

function limpiarCalendario() {
  const form = document.querySelector("#formCalendario form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Funciones para Reuniones
async function registrarReuniones(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/reuniones/crear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      alert("Registro guardado exitosamente");
      limpiarReuniones();
      buscarReuniones();
    } else {
      alert("Error al registrar: " + resultado.mensaje);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

async function buscarReuniones() {
  if (!checkAuthentication()) return;
  
  try {
    const response = await fetch('/api/tablas/reuniones/buscar');
    const resultados = await response.json();
    
    const tabla = document.getElementById("TablaReuniones");
    tabla.innerHTML = "";
    
    if (!resultados.success || !resultados.data || resultados.data.length === 0) {
      mostrarNoResultados('Reuniones', tabla);
      return;
    }

    resultados.data.forEach((registro) => {
      const fechaFormateada = formatearFecha(registro.fecha);
      const filaHtml = `
        <div data-id="${registro.id}">
          ${registro.id} | ${registro.Dirige} | ${registro.Lectura} | ${registro.Cantos_alegre} | ${registro.Ofrenda} | ${registro.Predica} | ${fechaFormateada}
          <div class="button-group">
            <button class="btn btn-primary" onclick="mostrarEditarReuniones('${registro.id}')">Editar</button>
            <button class="btn btn-secondary" onclick="eliminarReuniones('${registro.id}')">Eliminar</button>
          </div>
        </div>`;
      tabla.innerHTML += filaHtml;
    });
  } catch (error) {
    console.error('Error al buscar registros:', error);
    alert("Error al buscar registros: " + error.message);
  }
}

function limpiarReuniones() {
  const form = document.querySelector("#formReuniones form");
  form.reset();
  form.querySelector("[name='id']").value = '';
}

// Verificar autenticación al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  const verified = sessionStorage.getItem('userVerified') === 'true';
  if (verified) {
    // Mostrar botón de administradores si es admin
    const userRol = sessionStorage.getItem('userRol');
    if (userRol === 'Admin' || userRol === 'Super Admin') {
      const btnAdmins = document.getElementById('btnAdmins');
      if (btnAdmins) {
        btnAdmins.style.display = 'block';
      }
    }
  }
});
