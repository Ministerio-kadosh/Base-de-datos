Prompt para Remodelación de Base de Datos y Código
markdown
# 🛠️ Remodelación de Base de Datos y Refactorización de Código  
**Objetivo:** Actualizar estructura de base de datos y refactorizar código Python/JavaScript para alinearse con nueva definición de tablas.  

## 1. Cambios Clave en Base de Datos  
### Tablas Renombradas:  
- `predicadores` → Mantener  
- `reuniones` → Mantener  
- `calendario` → Mantener  
- `bandeja` → Mantener  
- `asistencias` → `asistencia`  
- `jovenes` → `jovenes` (mantener)  
- `finanzas` → `movimientos_financieros`  
- `historial_cambios` → Mantener  
- `informes` → `consultas` + `informes`  

### Cambios de Campos:  
```sql  
-- Asistencia  
ALTER TABLE asistencia RENAME COLUMN "Id_asistencia" TO id_asistencia;  
ALTER TABLE asistencia RENAME COLUMN "Id_Jovenes" TO id_joven;  
ALTER TABLE asistencia RENAME COLUMN "Fecha_viernes" TO fecha_reunion;  

-- Reuniones  
ALTER TABLE reuniones RENAME COLUMN "Id_Reuniones" TO id_reunion;  
ALTER TABLE reuniones RENAME COLUMN "Dirección" TO director;  
ALTER TABLE reuniones RENAME COLUMN "Oferida" TO ofrenda;  
2. Refactorización de Backend (Python)
Archivo tablas.py
python
# ANTES  
def buscar_predicadores_por_id(id=None):  
    response = supabase.table('predicadores').select('*').eq('id', id).execute()  

# DESPUÉS  
def buscar_predicadores_por_id(id=None):  
    response = supabase.table('predicadores').select('*').eq('id_predicador', id).execute()  
Archivo app.py - Actualizar Rutas CRUD:
python
# ANTES  
@app.route('/api/tablas/predicadores')  

# DESPUÉS  
@app.route('/api/tablas/predicadores', methods=['GET'])  
def api_obtener_predicadores():  
    id = request.args.get('id')  
    predicadores = buscar_predicadores_por_id(id)  
    # ... resto del código ...  
3. Refactorización de Frontend (JavaScript)
Archivo Tablas.html - Actualizar Formularios:
javascript
// ANTES  
function registrarPredicadores(e, form) {  
  const data = {  
    Nombre: form.Nombre.value,  
    Apellido: form.Apellido.value  
  };  
}  

// DESPUÉS  
function registrarPredicadores(e, form) {  
  const data = {  
    nombre: form.nombre.value,  
    apellido: form.apellido.value,  
    telefono: form.telefono.value  // Nuevo campo  
  };  
}  
4. Cambios en Relaciones de Datos
Nueva Estructura para Informes:
python
# consultas.py  
def crear_consulta(nombre, sql, parametros):  
    supabase.table('consultas').insert({  
        'nombre_consulta': nombre,  
        'sql_consulta': sql,  
        'parametros': json.dumps(parametros)  
    }).execute()  

# informes.py  
def generar_informe(id_consulta, parametros):  
    consulta = supabase.table('consultas').select('*').eq('id_consulta', id_consulta).execute()  
    # Ejecutar SQL con parámetros...  
5. Actualización de Endpoints
Nuevas Rutas API:
Ruta	Método	Descripción
/api/consultas	POST	Crear plantilla de consulta
/api/informes/generar	POST	Generar informe dinámico
/api/tablas/asistencia	GET	Obtener registros de asistencia
6. Reglas de Refactorización
Consistencia de Nombres:

Todos los campos en snake_case

Prefijos coherentes (id_, fecha_, nombre_)

Manejo de Errores:

python
try:  
    # Código actualizado  
except Exception as e:  
    logger.error(f"Error en función: {e}")  
    return {"error": str(e)}, 500  
Validación de Datos:

python
from pydantic import BaseModel  

class PredicadorModel(BaseModel):  
    nombre: str  
    apellido: str  
    telefono: str  
Documentación Post-Refactor:

Actualizar DOCUMENTACION_TECNICA.md con nuevos nombres

Generar nuevo diagrama de relaciones (opcional)

7. Checklist de Implementación
Ejecutar scripts de migración en Supabase

Refactorizar todas las funciones en tablas.py

Actualizar rutas en app.py

Modificar formularios en Tablas.html

Ajustar llamadas AJAX en JavaScript

Probar flujos CRUD completos

Verificar generación de informes

Ejemplo de Migración SQL (Supabase)
sql
-- Migrar tabla asistencias  
ALTER TABLE asistencias RENAME TO asistencia;  
ALTER TABLE asistencia RENAME COLUMN "Id_Jovenes" TO id_joven;  

-- Crear tabla consultas  
CREATE TABLE consultas (  
    id_consulta SERIAL PRIMARY KEY,  
    nombre_consulta VARCHAR(100) NOT NULL,  
    sql_consulta TEXT NOT NULL,  
    parametros JSONB,  
    id_admin_creador INTEGER REFERENCES administradores(id_admin)  
);  
Nota para la IA:

Priorizar cambios en tablas críticas: asistencia, reuniones, movimientos_financieros

Mantener compatibilidad con frontend durante transición

Usar logger para registrar cambios en lugar de print()

Asegurar que todas las FK usen nuevos nombres de campos

Generar scripts reversibles para migración

Beneficios Esperados
✅ Consistencia en todo el sistema
✅ Mejor mantenibilidad del código
✅ Preparación para futuras expansiones
✅ Documentación técnica actualizada

text

### Características clave del prompt:  
1. **Enfoque práctico**: Instrucciones específicas para cada capa (DB, backend, frontend)  
2. **Ejemplos concretos**: Muestra cambios reales de código antes/después  
3. **Gestión de transición**: Incluye checklist y consideraciones para migración  
4. **Supabase-ready**: Sintaxis SQL compatible con PostgreSQL  
5. **Extensible**: Preparado para agregar nuevas funcionalidades  

Este prompt guiará a la IA para realizar una refactorización completa y profesional del sistema, manteniendo la coherencia entre todos los componentes.




Tablas


### bandeja
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_bandeja     | SERIAL PRIMARY KEY  | Identificador único             |
| objetivo       | VARCHAR(255)        | Propósito de la bandeja         |
| descripcion    | TEXT                | Detalles del contenido          |

### asistencia
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_asistencia  | SERIAL PRIMARY KEY  | Identificador único             |
| id_joven       | INTEGER             | ID relacionado con jóvenes      |
| nombre_joven   | VARCHAR(100)        | Nombre completo del joven       |
| fecha_reunion  | DATE                | Fecha de reunión (viernes)      |
| asistio        | BOOLEAN             | Estado de asistencia (true/false) |

### jovenes
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_joven       | SERIAL PRIMARY KEY  | Identificador único             |
| nombre         | VARCHAR(100)        | Primer nombre                   |
| apellido       | VARCHAR(100)        | Apellido                        |
| telefono       | VARCHAR(20)         | Número de contacto              |
| fecha_registro | TIMESTAMP           | Fecha de registro en sistema    |

### movimientos_financieros
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_movimiento  | SERIAL PRIMARY KEY  | Identificador único             |
| tipo_movimiento| VARCHAR(50)         | Ingreso/Gasto                   |
| concepto       | VARCHAR(255)        | Descripción breve               |
| monto          | NUMERIC(10,2)       | Valor numérico                  |
| id_entidad     | INTEGER             | ID relacionado con entidades    |
| id_producto    | INTEGER             | ID relacionado con productos    |
| registrado_por | VARCHAR(100)        | Responsable de registro         |
| fecha_registro | TIMESTAMP           | Fecha de registro               |

### entidades_apoyo
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_entidad     | SERIAL PRIMARY KEY  | Identificador único             |
| nombre_entidad | VARCHAR(255)        | Nombre completo                 |
| tipo_entidad   | VARCHAR(50)         | Clasificación general           |
| contacto       | VARCHAR(100)        | Información de contacto         |
| es_donante     | BOOLEAN             | ¿Puede donar?                   |
| es_proveedor   | BOOLEAN             | ¿Provee productos?              |
| es_comercio    | BOOLEAN             | ¿Es lugar comercial?            |

### administradores
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_admin       | SERIAL PRIMARY KEY  | Identificador único             |
| nombre_admin   | VARCHAR(100)        | Nombre completo                 |
| rol_admin      | VARCHAR(50)         | Rol en sistema                  |
| codigo_acceso  | VARCHAR(20)         | Código de acceso                |
| fecha_registro | TIMESTAMP           | Fecha de registro               |

### predicadores
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_predicador  | SERIAL PRIMARY KEY  | Identificador único             |
| nombre         | VARCHAR(100)        | Primer nombre                   |
| apellido       | VARCHAR(100)        | Apellido                        |
| telefono       | VARCHAR(20)         | Número de contacto              |
| fecha_registro | TIMESTAMP           | Fecha de registro               |

### reuniones
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_reunion     | SERIAL PRIMARY KEY  | Identificador único             |
| director       | VARCHAR(255)        | Nombre del director             |
| lectura        | VARCHAR(100)        | Texto bíblico                   |
| cantos         | VARCHAR(255)        | Himnos/canciones                |
| ofrenda        | NUMERIC(10,2)       | Monto de ofrenda                |
| predicador     | VARCHAR(100)        | Nombre del predicador           |
| fecha_reunion  | DATE                | Fecha de reunión                |
| fecha_registro | TIMESTAMP           | Fecha de registro               |

### productos
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_producto    | SERIAL PRIMARY KEY  | Identificador único             |
| nombre_producto| VARCHAR(100)        | Nombre del producto             |
| precio_referencia | NUMERIC(10,2)    | Precio base                     |
| id_entidad     | INTEGER             | ID entidad proveedora           |

### calendario
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_evento      | SERIAL PRIMARY KEY  | Identificador único             |
| nombre_evento  | VARCHAR(255)        | Nombre del evento               |
| objetivo_evento| VARCHAR(255)        | Propósito del evento            |
| fecha_evento   | DATE                | Fecha programada                |
| observaciones  | TEXT                | Notas adicionales               |
| fecha_registro | TIMESTAMP           | Fecha de creación               |

### consultas
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_consulta    | SERIAL PRIMARY KEY  | Identificador único             |
| nombre_consulta| VARCHAR(100)        | Nombre descriptivo              |
| sql_consulta   | TEXT                | Consulta SQL parametrizada      |
| parametros     | JSONB               | Parámetros requeridos           |
| descripcion    | TEXT                | Explicación detallada           |
| id_admin_creador | INTEGER           | ID administrador creador        |
| fecha_creacion | TIMESTAMP           | Fecha de creación               |

### informes
| Campo          | Tipo de dato        | Descripción                     |
|----------------|---------------------|---------------------------------|
| id_informe     | SERIAL PRIMARY KEY  | Identificador único             |
| titulo_informe | VARCHAR(100)        | Título descriptivo              |
| id_consulta    | INTEGER             | ID consulta utilizada           |
| parametros_usados | JSONB            | Valores de parámetros usados    |
| formato_salida | VARCHAR(10)         | Formato (CSV/PDF/XLSX/HTML)     |
| estado         | VARCHAR(20)         | Estado (pendiente/generado/error)|
| resultados     | JSONB               | Datos resultantes               |
| id_usuario     | INTEGER             | ID usuario generador            |
| fecha_generacion | TIMESTAMP         | Fecha de generación             |