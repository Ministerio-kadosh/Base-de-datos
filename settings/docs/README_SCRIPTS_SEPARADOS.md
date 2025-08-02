# Instrucciones para Remodelación de Base de Datos con Scripts Separados

Para facilitar el proceso de remodelación de la base de datos y evitar errores, se han creado tres scripts SQL separados que pueden ejecutarse de forma independiente según sea necesario:

## 1. Eliminar Tablas y Políticas (`eliminar_tablas_politicas.sql`)

Este script se encarga de:
- Desactivar Row Level Security (RLS) en todas las tablas
- Eliminar todas las políticas de seguridad existentes
- Eliminar todas las tablas existentes en orden inverso de dependencia

**Cuándo usarlo**: 
- Cuando necesites eliminar completamente la estructura actual para comenzar desde cero
- Cuando tengas problemas con políticas de seguridad existentes
- Como primer paso en el proceso de remodelación

**Comando de ejecución**:
```sql
\i eliminar_tablas_politicas.sql
```

## 2. Crear Tablas (`remodelacion_limpia.sql`)

Este script se encarga de:
- Crear las 13 tablas con la estructura correcta
- Crear índices para optimización de consultas

**Cuándo usarlo**:
- Después de eliminar las tablas existentes
- Cuando necesites recrear solo la estructura de tablas sin políticas
- Como segundo paso en el proceso de remodelación

**Comando de ejecución**:
```sql
\i remodelacion_limpia.sql
```

## 3. Implementar Políticas de Seguridad (`politicas_seguridad.sql`)

Este script se encarga de:
- Habilitar Row Level Security (RLS) en todas las tablas
- Crear políticas de seguridad específicas para cada tabla y tipo de operación

**Cuándo usarlo**:
- Después de crear las tablas
- Cuando necesites implementar o actualizar solo las políticas de seguridad
- Como paso final en el proceso de remodelación

**Comando de ejecución**:
```sql
\i politicas_seguridad.sql
```

## Proceso Completo de Remodelación

Para realizar una remodelación completa, sigue estos pasos en orden:

1. **Copia de seguridad** (¡MUY IMPORTANTE!)
   ```sql
   \copy (SELECT * FROM tabla1) TO 'backup_tabla1.csv' WITH CSV HEADER;
   -- Repetir para cada tabla importante
   ```

2. **Eliminar estructura existente**
   ```sql
   \i eliminar_tablas_politicas.sql
   ```

3. **Crear nueva estructura de tablas**
   ```sql
   \i remodelacion_limpia.sql
   ```

4. **Implementar políticas de seguridad**
   ```sql
   \i politicas_seguridad.sql
   ```

5. **Restaurar datos** (si es necesario)
   ```sql
   \copy tabla1 FROM 'backup_tabla1.csv' WITH CSV HEADER;
   -- Repetir para cada tabla respaldada
   ```

## Solución de Problemas

- **Error al eliminar políticas**: Si encuentras errores al eliminar políticas, puedes intentar ejecutar solo la sección de eliminación de políticas del script `eliminar_tablas_politicas.sql`.

- **Error al crear tablas**: Verifica que todas las tablas anteriores hayan sido eliminadas correctamente antes de intentar crear las nuevas.

- **Error en políticas de seguridad**: Asegúrate de que todas las tablas existan antes de aplicar las políticas. Si encuentras errores específicos, puedes editar el script `politicas_seguridad.sql` para aplicar solo las políticas que necesites.

## Notas Importantes

- Estos scripts están diseñados para ser ejecutados en Supabase SQL Editor o mediante psql.
- Siempre realiza una copia de seguridad antes de ejecutar cualquier script que modifique la estructura de la base de datos.
- Los scripts utilizan la sintaxis `IF EXISTS` para evitar errores si las tablas o políticas no existen.
- Si necesitas personalizar algún aspecto, puedes editar los scripts según tus necesidades específicas.

---

Esta separación en tres scripts independientes facilita la gestión y solución de problemas durante el proceso de remodelación, permitiéndote ejecutar solo las partes necesarias según tu situación específica.