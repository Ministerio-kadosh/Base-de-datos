// Funciones para manejo de formularios en carrusel

// Variable para controlar el formulario activo
let formularioActivo = 'formBandeja';

// Función para mostrar formulario específico
function mostrarFormulario(formularioId) {
  if (!checkAuthentication()) return;
  
  // Ocultar todos los formularios
  document.querySelectorAll('.formulario-seccion').forEach(seccion => {
    seccion.style.display = 'none';
  });
  
  // Remover clase activa de todos los botones
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.remove('activo');
  });
  
  // Mostrar formulario seleccionado
  const formularioSeleccionado = document.getElementById(formularioId);
  if (formularioSeleccionado) {
    formularioSeleccionado.style.display = 'block';
    formularioActivo = formularioId;
  }
  
  // Marcar botón como activo
  const botonActivo = document.querySelector(`[onclick="mostrarFormulario('${formularioId}')"]`);
  if (botonActivo) {
    botonActivo.classList.add('activo');
  }
}

// Función para limpiar formulario
function limpiarFormulario(boton) {
  const formulario = boton.closest('form');
  if (formulario) {
    formulario.reset();
    limpiarErrores(formulario);
  }
}

// Función para limpiar errores de validación
function limpiarErrores(formulario) {
  formulario.querySelectorAll('.campo-error').forEach(campo => {
    campo.classList.remove('campo-error');
  });
  
  formulario.querySelectorAll('.mensaje-error').forEach(mensaje => {
    mensaje.remove();
  });
}

// Función para validar campo
function validarCampo(campo, reglas) {
  const valor = campo.value.trim();
  const nombreCampo = campo.name;
  
  // Limpiar errores previos
  campo.classList.remove('campo-error');
  const mensajeError = campo.parentNode.querySelector('.mensaje-error');
  if (mensajeError) {
    mensajeError.remove();
  }
  
  // Validar campo requerido
  if (reglas.requerido && !valor) {
    mostrarError(campo, `${nombreCampo} es requerido`);
    return false;
  }
  
  // Validar longitud mínima
  if (reglas.minLength && valor.length < reglas.minLength) {
    mostrarError(campo, `${nombreCampo} debe tener al menos ${reglas.minLength} caracteres`);
    return false;
  }
  
  // Validar longitud máxima
  if (reglas.maxLength && valor.length > reglas.maxLength) {
    mostrarError(campo, `${nombreCampo} debe tener máximo ${reglas.maxLength} caracteres`);
    return false;
  }
  
  // Validar patrón
  if (reglas.patron && !reglas.patron.test(valor)) {
    mostrarError(campo, reglas.mensajePatron || `${nombreCampo} no tiene el formato correcto`);
    return false;
  }
  
  // Validar email
  if (reglas.email && !validarEmail(valor)) {
    mostrarError(campo, `${nombreCampo} debe ser un email válido`);
    return false;
  }
  
  return true;
}

// Función para mostrar error
function mostrarError(campo, mensaje) {
  campo.classList.add('campo-error');
  
  const mensajeError = document.createElement('span');
  mensajeError.className = 'mensaje-error';
  mensajeError.textContent = mensaje;
  
  campo.parentNode.appendChild(mensajeError);
}

// Función para validar email
function validarEmail(email) {
  const patron = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return patron.test(email);
}

// Función para validar formulario completo
function validarFormulario(formulario) {
  let esValido = true;
  
  // Reglas de validación por campo
  const reglasValidacion = {
    'Objetivo': { requerido: true, minLength: 3, maxLength: 100 },
    'Descripcion': { requerido: true, minLength: 10, maxLength: 500 },
    'Nombre': { requerido: true, minLength: 2, maxLength: 50 },
    'Apellido': { requerido: true, minLength: 2, maxLength: 50 },
    'Numero': { requerido: true, patron: /^\d+$/, mensajePatron: 'El número debe contener solo dígitos' },
    'Dirige': { requerido: true, minLength: 2, maxLength: 50 },
    'Lectura': { requerido: true, minLength: 2, maxLength: 100 },
    'Cantos_alegre': { requerido: true, minLength: 2, maxLength: 100 },
    'Ofrenda': { requerido: true, minLength: 2, maxLength: 50 },
    'Predica': { requerido: true, minLength: 2, maxLength: 100 },
    'Concepto': { requerido: true, minLength: 3, maxLength: 100 },
    'Monto': { requerido: true, patron: /^\d+(\.\d{1,2})?$/, mensajePatron: 'El monto debe ser un número válido' },
    'Fecha': { requerido: true, patron: /^\d{4}-\d{2}-\d{2}$/, mensajePatron: 'La fecha debe tener formato YYYY-MM-DD' },
    'Observaciones': { requerido: true, minLength: 5, maxLength: 500 },
    'unoviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
    'dosviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
    'tresViernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
    'cuatroviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
    'cincoviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
    'Evento': { requerido: true, minLength: 3, maxLength: 100 }
  };
  
  // Validar cada campo del formulario
  formulario.querySelectorAll('input, textarea, select').forEach(campo => {
    if (campo.name && reglasValidacion[campo.name]) {
      if (!validarCampo(campo, reglasValidacion[campo.name])) {
        esValido = false;
      }
    }
  });
  
  return esValido;
}

// Función para mostrar mensaje de confirmación
function mostrarMensajeConfirmacion() {
  const mensaje = document.getElementById('mensajeConfirmacion');
  if (mensaje) {
    mensaje.style.display = 'flex';
  }
}

// Función para ocultar mensaje
function ocultarMensaje() {
  const mensaje = document.getElementById('mensajeConfirmacion');
  if (mensaje) {
    mensaje.style.display = 'none';
  }
}

// Funciones específicas para cada formulario

// Bandeja
async function registrarBandeja(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  // Mostrar pantalla de carga
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/formularios/bandeja', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Predicadores
async function registrarPredicadores(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/predicadores', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Reuniones
async function registrarReuniones(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/reuniones', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Finanzas
async function registrarFinanzas(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/formularios/finanzas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Asistencias
async function registrarAsistencias(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/formularios/asistencias', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Jóvenes
async function registrarJovenes(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/formularios/jovenes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Calendario
async function registrarCalendario(event, form) {
  event.preventDefault();
  if (!checkAuthentication()) return;
  
  if (!validarFormulario(form)) {
    alert('Por favor corrija los errores en el formulario');
    return;
  }
  
  const datos = Object.fromEntries(new FormData(form));
  datos.estado = 'Creado';
  datos.fecha = new Date().toISOString();
  
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    const response = await fetch('/api/tablas/calendario', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    
    document.getElementById('loadingOverlay').style.display = 'none';
    
    if (resultado.success) {
      mostrarMensajeConfirmacion();
      limpiarFormulario(form.querySelector('.btn-secondary'));
    } else {
      alert("Error al registrar: " + resultado.error);
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al registrar:', error);
    alert("Error al registrar: " + error.message);
  }
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Mostrar el primer formulario por defecto
  mostrarFormulario('formBandeja');
  
  // Agregar validación en tiempo real
  document.querySelectorAll('input, textarea, select').forEach(campo => {
    campo.addEventListener('blur', function() {
      const reglas = {
        'Objetivo': { requerido: true, minLength: 3, maxLength: 100 },
        'Descripcion': { requerido: true, minLength: 10, maxLength: 500 },
        'Nombre': { requerido: true, minLength: 2, maxLength: 50 },
        'Apellido': { requerido: true, minLength: 2, maxLength: 50 },
        'Numero': { requerido: true, patron: /^\d+$/, mensajePatron: 'El número debe contener solo dígitos' },
        'Dirige': { requerido: true, minLength: 2, maxLength: 50 },
        'Lectura': { requerido: true, minLength: 2, maxLength: 100 },
        'Cantos_alegre': { requerido: true, minLength: 2, maxLength: 100 },
        'Ofrenda': { requerido: true, minLength: 2, maxLength: 50 },
        'Predica': { requerido: true, minLength: 2, maxLength: 100 },
        'Concepto': { requerido: true, minLength: 3, maxLength: 100 },
        'Monto': { requerido: true, patron: /^\d+(\.\d{1,2})?$/, mensajePatron: 'El monto debe ser un número válido' },
        'Fecha': { requerido: true, patron: /^\d{4}-\d{2}-\d{2}$/, mensajePatron: 'La fecha debe tener formato YYYY-MM-DD' },
        'Observaciones': { requerido: true, minLength: 5, maxLength: 500 },
        'unoviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
        'dosviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
        'tresViernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
        'cuatroviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
        'cincoviernes': { requerido: true, patron: /^(Presente|Ausente|Justificado)$/, mensajePatron: 'Debe ser Presente, Ausente o Justificado' },
        'Evento': { requerido: true, minLength: 3, maxLength: 100 }
      };
      
      if (reglas[campo.name]) {
        validarCampo(campo, reglas[campo.name]);
      }
    });
  });
});
