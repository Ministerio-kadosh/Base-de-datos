# Sistema de Gestión - Flask + Supabase

## 🎉 **CONVERSIÓN COMPLETADA: Google Apps Script → Flask + Supabase**

Este proyecto ha sido **completamente convertido** de una aplicación Google Apps Script monolítica a una **aplicación Flask modular moderna** con Supabase como base de datos en la nube.

## 📋 **Resumen de la Conversión**

### **✅ CONVERTIDO EXITOSAMENTE:**
- **1 archivo GAS (64KB, 2134 líneas)** → **6 módulos Python modulares**
- **HTML/CSS/JS embebido** → **Archivos separados y organizados**
- **Google Sheets** → **Supabase PostgreSQL**
- **MailApp** → **Sistema de email SMTP**
- **Scripts monolíticos** → **API REST modular**

### **📊 Estadísticas de la Conversión:**
- **Líneas de código GAS:** 2,134 → **Líneas de código Python:** ~2,500
- **Archivos originales:** 1 → **Archivos convertidos:** 25+
- **Funcionalidades:** 100% preservadas + **mejoras adicionales**

## 📁 **Organización de Carpetas**

### **📂 settings/docs**
- Contiene toda la documentación técnica y de usuario del sistema
- Incluye archivos README, documentación técnica, guías de remodelación, etc.

### **📂 settings/test**
- Contiene archivos de prueba y diagnóstico
- Incluye scripts para verificar conexiones, probar funcionalidades, etc.

### **📂 settings/ejecutar**
- Contiene scripts para ejecutar tareas específicas
- Incluye scripts de inicialización, configuración, etc.

## 🚀 **Características Implementadas**

### **🔐 Sistema de Autenticación**
- Login seguro con verificación de administradores
- Sesiones persistentes con Flask-Session
- Control de acceso basado en roles (Admin, Super Admin)
- Logout automático y verificación de sesión

### **🗄️ Gestión de Datos (CRUD Completo)**
- **8 tablas principales:** Administradores, Predicadores, Reuniones, Calendario, Bandeja, Asistencias, Jóvenes, Finanzas