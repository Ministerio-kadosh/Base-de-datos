// Funciones para el manejo de informes y reportes
let plantillasGuardadas = [];
let historialInformes = [];
let informeActual = null;

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    cargarPlantillasGuardadas();
    cargarHistorialInformes();
    configurarEventos();
});

function configurarEventos() {
    // Evento para mostrar/ocultar fechas personalizadas
    const periodoSelect = document.getElementById('periodoInforme');
    if (periodoSelect) {
        periodoSelect.addEventListener('change', function() {
            const fechasPersonalizadas = document.getElementById('fechasPersonalizadas');
            if (this.value === 'personalizado') {
                fechasPersonalizadas.style.display = 'block';
            } else {
                fechasPersonalizadas.style.display = 'none';
            }
        });
    }

    // Eventos para filtros
    const filtros = document.querySelectorAll('.filtro-item input[type="checkbox"]');
    filtros.forEach(filtro => {
        filtro.addEventListener('change', function() {
            if (this.id === 'filtroActivos' && this.checked) {
                document.getElementById('filtroEliminados').checked = false;
            }
            if (this.id === 'filtroEliminados' && this.checked) {
                document.getElementById('filtroActivos').checked = false;
            }
        });
    });
}

function cambiarTipoInforme() {
    const tipoInforme = document.getElementById('tipoInforme').value;
    const contenidoPrevia = document.getElementById('contenidoPrevia');
    
    if (!tipoInforme) {
        contenidoPrevia.innerHTML = '<p class="mensaje-inicial">Seleccione un tipo de informe y haga clic en "Vista Previa"</p>';
        return;
    }

    // Mostrar información básica del tipo de informe
    let descripcion = '';
    switch (tipoInforme) {
        case 'resumen':
            descripcion = 'Informe general con estadísticas de todas las tablas principales';
            break;
        case 'financiero':
            descripcion = 'Reporte detallado de ingresos, gastos y balance financiero';
            break;
        case 'asistencias':
            descripcion = 'Análisis de asistencia a reuniones y actividades';
            break;
        case 'actividades':
            descripcion = 'Resumen de actividades y eventos realizados';
            break;
        case 'personalizado':
            descripcion = 'Informe personalizado con consultas específicas';
            break;
    }

    contenidoPrevia.innerHTML = `
        <div class="info-informe">
            <h4>Tipo de Informe: ${tipoInforme.toUpperCase()}</h4>
            <p>${descripcion}</p>
            <p>Haga clic en "Vista Previa" para generar el informe completo.</p>
        </div>
    `;
}

async function generarInforme() {
    try {
        mostrarCargando();
        
        const tipoInforme = document.getElementById('tipoInforme').value;
        if (!tipoInforme) {
            mostrarError('Debe seleccionar un tipo de informe');
            return;
        }

        const datos = recopilarDatosInforme();
        
        // Llamada al backend para generar el informe
        const response = await fetch('/api/informes/generar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) {
            throw new Error('Error al generar el informe');
        }

        const resultado = await response.json();
        informeActual = resultado;
        
        // Mostrar vista previa
        mostrarVistaPrevia(resultado);
        
        // Actualizar estadísticas
        mostrarEstadisticas(resultado.estadisticas);
        
        // Guardar en historial
        guardarEnHistorial(resultado);
        
        mostrarExito('Informe generado exitosamente');
        
    } catch (error) {
        console.error('Error al generar informe:', error);
        mostrarError('Error al generar el informe: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

async function vistaPrevia() {
    try {
        mostrarCargando();
        
        const tipoInforme = document.getElementById('tipoInforme').value;
        if (!tipoInforme) {
            mostrarError('Debe seleccionar un tipo de informe');
            return;
        }

        const datos = recopilarDatosInforme();
        
        // Llamada al backend para vista previa
        const response = await fetch('/api/informes/previa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) {
            throw new Error('Error al generar vista previa');
        }

        const resultado = await response.json();
        
        // Mostrar vista previa
        mostrarVistaPrevia(resultado);
        
        mostrarExito('Vista previa generada');
        
    } catch (error) {
        console.error('Error al generar vista previa:', error);
        mostrarError('Error al generar vista previa: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

function recopilarDatosInforme() {
    const tipoInforme = document.getElementById('tipoInforme').value;
    const periodo = document.getElementById('periodoInforme').value;
    const fechaInicio = document.getElementById('fechaInicio')?.value;
    const fechaFin = document.getElementById('fechaFin')?.value;
    
    // Recopilar filtros
    const filtros = {
        activos: document.getElementById('filtroActivos').checked,
        eliminados: document.getElementById('filtroEliminados').checked,
        historial: document.getElementById('filtroHistorial').checked
    };
    
    // Recopilar formato
    const formato = document.querySelector('input[name="formato"]:checked')?.value || 'pdf';
    
    return {
        tipo: tipoInforme,
        periodo: periodo,
        fechaInicio: fechaInicio,
        fechaFin: fechaFin,
        filtros: filtros,
        formato: formato
    };
}

function mostrarVistaPrevia(resultado) {
    const contenidoPrevia = document.getElementById('contenidoPrevia');
    
    if (!resultado || !resultado.datos) {
        contenidoPrevia.innerHTML = '<p class="error">No se pudieron obtener los datos del informe</p>';
        return;
    }

    let html = `
        <div class="informe-preview">
            <div class="header-informe">
                <h3>${resultado.titulo || 'Informe Generado'}</h3>
                <p class="fecha-generacion">Generado el: ${new Date().toLocaleString()}</p>
            </div>
    `;

    // Mostrar datos según el tipo de informe
    if (resultado.datos.resumen) {
        html += mostrarResumenGeneral(resultado.datos.resumen);
    } else if (resultado.datos.financiero) {
        html += mostrarReporteFinanciero(resultado.datos.financiero);
    } else if (resultado.datos.asistencias) {
        html += mostrarReporteAsistencias(resultado.datos.asistencias);
    } else if (resultado.datos.actividades) {
        html += mostrarReporteActividades(resultado.datos.actividades);
    } else {
        html += mostrarDatosGenericos(resultado.datos);
    }

    html += '</div>';
    contenidoPrevia.innerHTML = html;
}

function mostrarResumenGeneral(datos) {
    return `
        <div class="seccion-informe">
            <h4>Resumen General</h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-numero">${datos.totalPredicadores || 0}</span>
                    <span class="stat-label">Predicadores</span>
                </div>
                <div class="stat-item">
                    <span class="stat-numero">${datos.totalJovenes || 0}</span>
                    <span class="stat-label">Jóvenes</span>
                </div>
                <div class="stat-item">
                    <span class="stat-numero">${datos.totalReuniones || 0}</span>
                    <span class="stat-label">Reuniones</span>
                </div>
                <div class="stat-item">
                    <span class="stat-numero">${datos.totalAsistencias || 0}</span>
                    <span class="stat-label">Asistencias</span>
                </div>
            </div>
        </div>
    `;
}

function mostrarReporteFinanciero(datos) {
    return `
        <div class="seccion-informe">
            <h4>Reporte Financiero</h4>
            <div class="finanzas-summary">
                <div class="finanza-item ingresos">
                    <h5>Ingresos</h5>
                    <span class="monto">$${datos.totalIngresos || 0}</span>
                </div>
                <div class="finanza-item gastos">
                    <h5>Gastos</h5>
                    <span class="monto">$${datos.totalGastos || 0}</span>
                </div>
                <div class="finanza-item balance">
                    <h5>Balance</h5>
                    <span class="monto ${(datos.balance || 0) >= 0 ? 'positivo' : 'negativo'}">
                        $${datos.balance || 0}
                    </span>
                </div>
            </div>
            ${datos.transacciones ? mostrarTablaTransacciones(datos.transacciones) : ''}
        </div>
    `;
}

function mostrarReporteAsistencias(datos) {
    return `
        <div class="seccion-informe">
            <h4>Reporte de Asistencias</h4>
            <div class="asistencias-summary">
                <div class="asistencia-item">
                    <span class="stat-numero">${datos.totalAsistencias || 0}</span>
                    <span class="stat-label">Total Asistencias</span>
                </div>
                <div class="asistencia-item">
                    <span class="stat-numero">${datos.promedioAsistencia || 0}%</span>
                    <span class="stat-label">Promedio de Asistencia</span>
                </div>
            </div>
            ${datos.detalleAsistencias ? mostrarTablaAsistencias(datos.detalleAsistencias) : ''}
        </div>
    `;
}

function mostrarReporteActividades(datos) {
    return `
        <div class="seccion-informe">
            <h4>Reporte de Actividades</h4>
            <div class="actividades-summary">
                <div class="actividad-item">
                    <span class="stat-numero">${datos.totalActividades || 0}</span>
                    <span class="stat-label">Total Actividades</span>
                </div>
                <div class="actividad-item">
                    <span class="stat-numero">${datos.actividadesCompletadas || 0}</span>
                    <span class="stat-label">Completadas</span>
                </div>
            </div>
            ${datos.actividades ? mostrarTablaActividades(datos.actividades) : ''}
        </div>
    `;
}

function mostrarDatosGenericos(datos) {
    let html = '<div class="seccion-informe"><h4>Datos del Informe</h4>';
    
    if (Array.isArray(datos)) {
        html += '<div class="tabla-datos"><table><thead><tr>';
        if (datos.length > 0) {
            Object.keys(datos[0]).forEach(key => {
                html += `<th>${key}</th>`;
            });
        }
        html += '</tr></thead><tbody>';
        
        datos.forEach(fila => {
            html += '<tr>';
            Object.values(fila).forEach(valor => {
                html += `<td>${valor}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table></div>';
    } else {
        html += '<pre>' + JSON.stringify(datos, null, 2) + '</pre>';
    }
    
    html += '</div>';
    return html;
}

function mostrarTablaTransacciones(transacciones) {
    if (!Array.isArray(transacciones) || transacciones.length === 0) {
        return '<p>No hay transacciones para mostrar</p>';
    }

    let html = '<div class="tabla-transacciones"><table><thead><tr>';
    html += '<th>Fecha</th><th>Descripción</th><th>Tipo</th><th>Monto</th>';
    html += '</tr></thead><tbody>';

    transacciones.forEach(trans => {
        html += `<tr>
            <td>${trans.fecha || ''}</td>
            <td>${trans.descripcion || ''}</td>
            <td>${trans.tipo || ''}</td>
            <td class="${trans.tipo === 'ingreso' ? 'positivo' : 'negativo'}">
                $${trans.monto || 0}
            </td>
        </tr>`;
    });

    html += '</tbody></table></div>';
    return html;
}

function mostrarTablaAsistencias(asistencias) {
    if (!Array.isArray(asistencias) || asistencias.length === 0) {
        return '<p>No hay datos de asistencia para mostrar</p>';
    }

    let html = '<div class="tabla-asistencias"><table><thead><tr>';
    html += '<th>Fecha</th><th>Actividad</th><th>Asistentes</th><th>Porcentaje</th>';
    html += '</tr></thead><tbody>';

    asistencias.forEach(asist => {
        html += `<tr>
            <td>${asist.fecha || ''}</td>
            <td>${asist.actividad || ''}</td>
            <td>${asist.asistentes || 0}</td>
            <td>${asist.porcentaje || 0}%</td>
        </tr>`;
    });

    html += '</tbody></table></div>';
    return html;
}

function mostrarTablaActividades(actividades) {
    if (!Array.isArray(actividades) || actividades.length === 0) {
        return '<p>No hay actividades para mostrar</p>';
    }

    let html = '<div class="tabla-actividades"><table><thead><tr>';
    html += '<th>Fecha</th><th>Actividad</th><th>Estado</th><th>Participantes</th>';
    html += '</tr></thead><tbody>';

    actividades.forEach(act => {
        html += `<tr>
            <td>${act.fecha || ''}</td>
            <td>${act.nombre || ''}</td>
            <td><span class="estado ${act.estado || ''}">${act.estado || ''}</span></td>
            <td>${act.participantes || 0}</td>
        </tr>`;
    });

    html += '</tbody></table></div>';
    return html;
}

function mostrarEstadisticas(estadisticas) {
    const contenedor = document.getElementById('estadisticasInforme');
    if (!estadisticas || !contenedor) return;

    let html = '';
    
    Object.entries(estadisticas).forEach(([categoria, datos]) => {
        html += `<div class="stat-categoria">
            <h4>${categoria}</h4>
            <div class="stat-items">`;
        
        Object.entries(datos).forEach(([clave, valor]) => {
            html += `<div class="stat-item">
                <span class="stat-label">${clave}</span>
                <span class="stat-valor">${valor}</span>
            </div>`;
        });
        
        html += '</div></div>';
    });

    contenedor.innerHTML = html;
}

async function guardarPlantilla() {
    try {
        const nombre = prompt('Ingrese un nombre para la plantilla:');
        if (!nombre) return;

        const datos = recopilarDatosInforme();
        datos.nombre = nombre;
        datos.fechaCreacion = new Date().toISOString();

        // Guardar en localStorage por ahora (en producción sería en base de datos)
        plantillasGuardadas.push(datos);
        localStorage.setItem('plantillasInformes', JSON.stringify(plantillasGuardadas));

        cargarPlantillasGuardadas();
        mostrarExito('Plantilla guardada exitosamente');

    } catch (error) {
        console.error('Error al guardar plantilla:', error);
        mostrarError('Error al guardar la plantilla');
    }
}

async function cargarPlantillasGuardadas() {
    try {
        // Cargar desde localStorage por ahora
        const plantillas = localStorage.getItem('plantillasInformes');
        plantillasGuardadas = plantillas ? JSON.parse(plantillas) : [];

        const contenedor = document.getElementById('listaPlantillas');
        if (!contenedor) return;

        if (plantillasGuardadas.length === 0) {
            contenedor.innerHTML = '<p class="sin-plantillas">No hay plantillas guardadas</p>';
            return;
        }

        let html = '';
        plantillasGuardadas.forEach((plantilla, index) => {
            html += `
                <div class="plantilla-item">
                    <div class="plantilla-info">
                        <h4>${plantilla.nombre}</h4>
                        <p>Tipo: ${plantilla.tipo}</p>
                        <p>Creada: ${new Date(plantilla.fechaCreacion).toLocaleDateString()}</p>
                    </div>
                    <div class="plantilla-acciones">
                        <button onclick="cargarPlantilla(${index})" class="btn btn-sm btn-primary">Cargar</button>
                        <button onclick="eliminarPlantilla(${index})" class="btn btn-sm btn-danger">Eliminar</button>
                    </div>
                </div>
            `;
        });

        contenedor.innerHTML = html;

    } catch (error) {
        console.error('Error al cargar plantillas:', error);
    }
}

function cargarPlantilla(index) {
    const plantilla = plantillasGuardadas[index];
    if (!plantilla) return;

    // Cargar datos en el formulario
    document.getElementById('tipoInforme').value = plantilla.tipo || '';
    document.getElementById('periodoInforme').value = plantilla.periodo || '';
    
    if (plantilla.fechaInicio) {
        document.getElementById('fechaInicio').value = plantilla.fechaInicio;
    }
    if (plantilla.fechaFin) {
        document.getElementById('fechaFin').value = plantilla.fechaFin;
    }

    // Cargar filtros
    if (plantilla.filtros) {
        document.getElementById('filtroActivos').checked = plantilla.filtros.activos || false;
        document.getElementById('filtroEliminados').checked = plantilla.filtros.eliminados || false;
        document.getElementById('filtroHistorial').checked = plantilla.filtros.historial || false;
    }

    // Cargar formato
    if (plantilla.formato) {
        document.querySelector(`input[name="formato"][value="${plantilla.formato}"]`).checked = true;
    }

    cambiarTipoInforme();
    mostrarExito('Plantilla cargada exitosamente');
}

function eliminarPlantilla(index) {
    if (!confirm('¿Está seguro de que desea eliminar esta plantilla?')) return;

    plantillasGuardadas.splice(index, 1);
    localStorage.setItem('plantillasInformes', JSON.stringify(plantillasGuardadas));
    cargarPlantillasGuardadas();
    mostrarExito('Plantilla eliminada');
}

async function enviarPorEmail() {
    if (!informeActual) {
        mostrarError('Debe generar un informe primero');
        return;
    }

    const email = prompt('Ingrese la dirección de email del destinatario:');
    if (!email) return;

    try {
        mostrarCargando();
        
        const response = await fetch('/api/informes/enviar-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                idInforme: informeActual.id,
                destinatario: email
            })
        });

        if (!response.ok) {
            throw new Error('Error al enviar el email');
        }

        mostrarExito('Informe enviado por email exitosamente');

    } catch (error) {
        console.error('Error al enviar email:', error);
        mostrarError('Error al enviar el email: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

async function descargarInforme() {
    if (!informeActual) {
        mostrarError('Debe generar un informe primero');
        return;
    }

    try {
        mostrarCargando();
        
        const formato = document.querySelector('input[name="formato"]:checked')?.value || 'pdf';
        
        const response = await fetch(`/api/informes/descargar/${informeActual.id}?formato=${formato}`, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Error al descargar el informe');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `informe_${new Date().toISOString().split('T')[0]}.${formato}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        mostrarExito('Informe descargado exitosamente');

    } catch (error) {
        console.error('Error al descargar informe:', error);
        mostrarError('Error al descargar el informe: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

function guardarEnHistorial(informe) {
    const historialItem = {
        id: Date.now(),
        titulo: informe.titulo || 'Informe sin título',
        tipo: informe.tipo || 'desconocido',
        fecha: new Date().toISOString(),
        formato: informe.formato || 'pdf'
    };

    historialInformes.unshift(historialItem);
    
    // Mantener solo los últimos 50 informes
    if (historialInformes.length > 50) {
        historialInformes = historialInformes.slice(0, 50);
    }

    localStorage.setItem('historialInformes', JSON.stringify(historialInformes));
    cargarHistorialInformes();
}

function cargarHistorialInformes() {
    try {
        const historial = localStorage.getItem('historialInformes');
        historialInformes = historial ? JSON.parse(historial) : [];

        const contenedor = document.getElementById('historialInformes');
        if (!contenedor) return;

        if (historialInformes.length === 0) {
            contenedor.innerHTML = '<p class="sin-historial">No hay historial de informes</p>';
            return;
        }

        let html = '<table><thead><tr>';
        html += '<th>Fecha</th><th>Título</th><th>Tipo</th><th>Formato</th><th>Acciones</th>';
        html += '</tr></thead><tbody>';

        historialInformes.forEach(item => {
            html += `<tr>
                <td>${new Date(item.fecha).toLocaleDateString()}</td>
                <td>${item.titulo}</td>
                <td>${item.tipo}</td>
                <td>${item.formato.toUpperCase()}</td>
                <td>
                    <button onclick="descargarInformeHistorial(${item.id})" class="btn btn-sm btn-primary">Descargar</button>
                </td>
            </tr>`;
        });

        html += '</tbody></table>';
        contenedor.innerHTML = html;

    } catch (error) {
        console.error('Error al cargar historial:', error);
    }
}

async function descargarInformeHistorial(id) {
    const item = historialInformes.find(h => h.id === id);
    if (!item) {
        mostrarError('Informe no encontrado en el historial');
        return;
    }

    try {
        mostrarCargando();
        
        const response = await fetch(`/api/informes/descargar/${id}?formato=${item.formato}`, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Error al descargar el informe');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${item.titulo}_${new Date(item.fecha).toISOString().split('T')[0]}.${item.formato}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        mostrarExito('Informe descargado exitosamente');

    } catch (error) {
        console.error('Error al descargar informe del historial:', error);
        mostrarError('Error al descargar el informe: ' + error.message);
    } finally {
        ocultarCargando();
    }
}

// Funciones de utilidad
function mostrarCargando() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.style.display = 'flex';
}

function ocultarCargando() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.style.display = 'none';
}

function mostrarExito(mensaje) {
    mostrarNotificacion(mensaje, 'exito');
}

function mostrarError(mensaje) {
    mostrarNotificacion(mensaje, 'error');
}

function mostrarNotificacion(mensaje, tipo) {
    // Crear notificación temporal
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    notificacion.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 10000;
        ${tipo === 'exito' ? 'background-color: #4CAF50;' : 'background-color: #f44336;'}
    `;

    document.body.appendChild(notificacion);

    // Remover después de 3 segundos
    setTimeout(() => {
        if (notificacion.parentNode) {
            notificacion.parentNode.removeChild(notificacion);
        }
    }, 3000);
}
