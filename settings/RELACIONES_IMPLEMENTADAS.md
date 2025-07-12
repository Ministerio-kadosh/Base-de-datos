# Relaciones Implementadas Entre Tablas

## 📊 **Estructura de Relaciones**

### 🔗 **Relaciones Principales**

#### 1. **Asistencias ↔ Jóvenes**
- **Campo**: `asistencias.joven_id` → `jovenes.id`
- **Tipo**: Foreign Key con CASCADE SET NULL
- **Propósito**: Relacionar asistencias con jóvenes específicos
- **Consulta**: `/api/consultas/asistencias-joven`

#### 2. **Reuniones ↔ Predicadores**
- **Campo**: `reuniones.predicador_id` → `predicadores.id`
- **Tipo**: Foreign Key con CASCADE SET NULL
- **Propósito**: Relacionar reuniones con predicadores que las dirigen
- **Consulta**: `/api/consultas/reuniones-predicador`

#### 3. **Finanzas ↔ Reuniones**
- **Campo**: `finanzas.reunion_id` → `reuniones.id`
- **Tipo**: Foreign Key con CASCADE SET NULL
- **Propósito**: Relacionar finanzas con reuniones específicas
- **Consulta**: `/api/consultas/finanzas-reunion`

#### 4. **Calendario ↔ Reuniones**
- **Campo**: `calendario.reunion_id` → `reuniones.id`
- **Tipo**: Foreign Key con CASCADE SET NULL
- **Propósito**: Relacionar eventos del calendario con reuniones
- **Consulta**: `/api/consultas/calendario-reunion`

#### 5. **Asistencias ↔ Reuniones**
- **Campo**: `asistencias.reunion_id` → `reuniones.id`
- **Tipo**: Foreign Key con CASCADE SET NULL
- **Propósito**: Relacionar asistencias con reuniones específicas

## 🆕 **Nuevas Funcionalidades**

### 📅 **Campo Fecha en Reuniones**
- **Campo**: `fecha_reunion` (DATE)
- **Propósito**: Fecha específica de la reunión
- **Formulario**: Agregado al formulario de Reuniones

### 🔧 **Consultas con Relaciones**

#### **Consulta General con Relaciones**
```javascript
POST /api/consultas/relaciones
{
  "tabla": "reuniones",
  "relaciones": ["predicadores", "asistencias"],
  "filtros": {"fecha_reunion": {"gte": "2024-01-01"}},
  "ordenamiento": {"fecha_reunion": "desc"},
  "limite": 10
}
```

#### **Consulta Reuniones con Predicador**
```javascript
POST /api/consultas/reuniones-predicador
{
  "filtros": {"fecha_reunion": "2024-01-15"}
}
```

#### **Consulta Asistencias con Joven**
```javascript
POST /api/consultas/asistencias-joven
{
  "filtros": {"joven_id": 1}
}
```

#### **Consulta Finanzas con Reunión**
```javascript
POST /api/consultas/finanzas-reunion
{
  "filtros": {"reunion_id": 1}
}
```

#### **Consulta Completa de Reunión**
```javascript
POST /api/consultas/reunion-completa
{
  "fecha_inicio": "2024-01-01",
  "fecha_fin": "2024-01-31"
}
```

#### **Estadísticas con Relaciones**
```javascript
GET /api/consultas/estadisticas-relacionadas
```

## 📈 **Estadísticas Disponibles**

### **Predicadores**
- Total de reuniones dirigidas por predicador
- Información completa del predicador

### **Jóvenes**
- Total de asistencias por joven
- Asistencias presentes vs ausentes
- Información demográfica

### **Finanzas por Reunión**
- Monto total recaudado por reunión
- Desglose de conceptos
- Tendencias temporales

## 🔧 **Implementación Técnica**

### **Script SQL**
```sql
-- Relaciones agregadas automáticamente
ALTER TABLE asistencias ADD COLUMN joven_id INTEGER REFERENCES jovenes(id);
ALTER TABLE reuniones ADD COLUMN predicador_id INTEGER REFERENCES predicadores(id);
ALTER TABLE finanzas ADD COLUMN reunion_id INTEGER REFERENCES reuniones(id);
ALTER TABLE calendario ADD COLUMN reunion_id INTEGER REFERENCES reuniones(id);
ALTER TABLE asistencias ADD COLUMN reunion_id INTEGER REFERENCES reuniones(id);

-- Índices para optimización
CREATE INDEX idx_asistencias_joven_id ON asistencias(joven_id);
CREATE INDEX idx_reuniones_predicador_id ON reuniones(predicador_id);
CREATE INDEX idx_finanzas_reunion_id ON finanzas(reunion_id);
CREATE INDEX idx_calendario_reunion_id ON calendario(reunion_id);
CREATE INDEX idx_asistencias_reunion_id ON asistencias(reunion_id);
```

### **Funciones Python**
- `consulta_con_relaciones()` - Consulta general con relaciones
- `consulta_reuniones_con_predicador()` - Reuniones + predicador
- `consulta_asistencias_con_joven()` - Asistencias + joven
- `consulta_finanzas_con_reunion()` - Finanzas + reunión
- `consulta_calendario_con_reunion()` - Calendario + reunión
- `consulta_completa_reunion()` - Reunión completa con todos los datos
- `consulta_estadisticas_relacionadas()` - Estadísticas con relaciones

## 🎯 **Casos de Uso**

### **1. Reporte de Reunión Completa**
- Información de la reunión
- Predicador que dirigió
- Lista de asistencias con jóvenes
- Finanzas recaudadas
- Eventos del calendario relacionados

### **2. Seguimiento de Jóvenes**
- Asistencias por joven
- Tendencias de participación
- Relación con reuniones específicas

### **3. Análisis de Predicadores**
- Reuniones dirigidas por predicador
- Frecuencia de participación
- Rendimiento y seguimiento

### **4. Control Financiero**
- Finanzas por reunión
- Tendencias de recaudación
- Relación con eventos específicos

## ⚠️ **Notas Importantes**

1. **Compatibilidad**: Las relaciones son opcionales (NULL permitido)
2. **Integridad**: CASCADE SET NULL para mantener integridad referencial
3. **Performance**: Índices creados para optimizar consultas
4. **Flexibilidad**: Se pueden hacer consultas con o sin relaciones

## 🚀 **Próximos Pasos**

1. **Ejecutar script SQL** para crear relaciones
2. **Probar consultas** con relaciones
3. **Implementar en frontend** las nuevas opciones de consulta
4. **Crear reportes** que aprovechen las relaciones

## 📞 **Soporte**

Para problemas con relaciones:
- Verificar que las tablas existan
- Confirmar que los IDs sean válidos
- Revisar logs de consultas
- Probar consultas individuales antes de combinadas 