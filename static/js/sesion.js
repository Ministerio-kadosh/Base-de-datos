// Verificación de acceso
let userVerified = false;

// Función para encriptar contraseñas
async function encriptarPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// Función de verificación de acceso
async function verificarAcceso(event) {
  event.preventDefault();
  const form = event.target;
  const datos = Object.fromEntries(new FormData(form));
  
  // Validar que todos los campos estén completos
  if (!datos.email || !datos.nombre || !datos.codigo) {
    const errorDiv = document.getElementById('verificationError');
    errorDiv.textContent = 'Por favor complete todos los campos';
    errorDiv.style.display = 'block';
    return;
  }

  // Limpiar espacios en blanco
  datos.email = datos.email.trim();
  datos.nombre = datos.nombre.trim();
  datos.codigo = datos.codigo.trim();

  // Mostrar loading mientras se verifica
  document.getElementById('loadingOverlay').style.display = 'flex';
  
  try {
    // Encriptar el código de acceso
    const codigoEncriptado = await encriptarPassword(datos.codigo);
    
    // Llamar al backend para verificar
    const response = await fetch('/api/sesion/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: datos.email,
        nombre: datos.nombre,
        codigo: datos.codigo  // Enviar código sin encriptar
      })
    });

    const resultado = await response.json();
    
    if (resultado.success) {
      // Guardar datos de sesión
      sessionStorage.setItem('userEmail', datos.email);
      sessionStorage.setItem('userNombre', datos.nombre);
      sessionStorage.setItem('userRol', resultado.rol || 'Usuario');
      sessionStorage.setItem('userVerified', 'true');
      
      userVerified = true;
      
      // Ocultar pantalla de verificación
      document.getElementById('verificationScreen').style.display = 'none';
      document.getElementById('loadingOverlay').style.display = 'none';
      
      // Mostrar menú principal
      document.getElementById('menu').classList.add('visible');
      
      // Mostrar botón de administradores si es admin
      if (resultado.rol === 'Admin' || resultado.rol === 'Super Admin') {
        document.getElementById('btnAdmins').style.display = 'block';
      }
      
      // Mostrar mensaje de bienvenida
      const authMessage = document.getElementById('authMessage');
      if (authMessage) {
        authMessage.innerHTML = `
          <h2>Bienvenido, ${datos.nombre}!</h2>
          <p>Sesión iniciada correctamente. Seleccione una opción del menú para continuar.</p>
        `;
      }
    } else {
      document.getElementById('loadingOverlay').style.display = 'none';
      const errorDiv = document.getElementById('verificationError');
      errorDiv.textContent = resultado.mensaje || 'Credenciales inválidas';
      errorDiv.style.display = 'block';
    }
  } catch (error) {
    document.getElementById('loadingOverlay').style.display = 'none';
    console.error('Error al verificar acceso:', error);
    const errorDiv = document.getElementById('verificationError');
    errorDiv.textContent = 'Error de conexión. Intente nuevamente.';
    errorDiv.style.display = 'block';
  }
}

// Función para verificar autenticación
function checkAuthentication() {
  const verified = sessionStorage.getItem('userVerified') === 'true';
  if (!verified) {
    alert('Por favor inicie sesión para continuar');
    window.location.href = '/';
    return false;
  }
  return true;
}

// Función para cerrar sesión
function cerrarSesion() {
  if (confirm('¿Está seguro que desea cerrar sesión?')) {
    // Limpiar datos de sesión
    sessionStorage.clear();
    userVerified = false;
    
    // Redirigir a la página de login
    window.location.href = '/';
  }
}

// Función para volver al menú
function volverAlMenu() {
  document.querySelectorAll('.seccion').forEach(s => s.classList.remove('visible'));
  document.getElementById('menu').classList.add('visible');
}

// Función para mostrar sección
function mostrarSeccion(seccionId) {
  if (!checkAuthentication()) return;
  
  document.querySelectorAll('.seccion').forEach(s => s.classList.remove('visible'));
  document.getElementById('menu').classList.remove('visible');
  document.getElementById(seccionId).classList.add('visible');
}

// Función para cerrar modales
function cerrarModalNoResultados() {
  document.getElementById('modalNoResultados').style.display = 'none';
}

// Función para mostrar modal de no resultados
function mostrarModalNoResultados(tabla) {
  const modal = document.getElementById('modalNoResultados');
  modal.dataset.tablaActual = tabla;
  modal.style.display = 'block';
}

// Función para mostrar no resultados
function mostrarNoResultados(tabla, contenedor) {
  mostrarModalNoResultados(tabla);
  if (contenedor) {
    contenedor.innerHTML = '<div class="error-message">No se encontraron registros</div>';
  }
}

// Función para formatear fechas
function formatearFecha(fecha) {
  if (!fecha) return 'N/A';
  try {
    const fechaObj = new Date(fecha);
    if (isNaN(fechaObj)) return 'N/A';
    
    const opciones = {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    };
    
    return fechaObj.toLocaleDateString('es-ES', opciones).replace(/,/g, '');
  } catch (e) {
    console.error('Error al formatear fecha:', e);
    return 'N/A';
  }
}

// Función para normalizar estado
function normalizarEstado(estado) {
  if (!estado) return 'Activo';
  return estado;
}

// Función para validar ID
function validarId(id) {
  const numericId = parseInt(id);
  if (isNaN(numericId)) {
    throw new Error('ID inválido');
  }
  return numericId;
}

// Verificar autenticación al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  const verified = sessionStorage.getItem('userVerified') === 'true';
  if (verified) {
    // userVerified ya está declarada arriba, solo asignamos
    userVerified = true;
    document.getElementById('verificationScreen').style.display = 'none';
    document.getElementById('menu').classList.add('visible');
    
    // Mostrar botón de administradores si es admin
    const userRol = sessionStorage.getItem('userRol');
    if (userRol === 'Admin' || userRol === 'Super Admin') {
      const btnAdmins = document.getElementById('btnAdmins');
      if (btnAdmins) {
        btnAdmins.style.display = 'block';
      }
    }
    
    // Mostrar mensaje de bienvenida
    const userNombre = sessionStorage.getItem('userNombre');
    const authMessage = document.getElementById('authMessage');
    if (authMessage && userNombre) {
      authMessage.innerHTML = `
        <h2>Bienvenido, ${userNombre}!</h2>
        <p>Sesión activa. Seleccione una opción del menú para continuar.</p>
      `;
    }
  }
});
