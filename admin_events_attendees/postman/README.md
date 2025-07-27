# 📮 Colección de Postman - Admin Events Microservicio

Esta carpeta contiene las colecciones y environments de Postman para probar completamente el microservicio de gestión de asistentes con todas las funcionalidades de seguridad implementadas.

## 📁 Archivos Incluidos

### 🧪 Colecciones de Pruebas

1. **`Admin_Events_Enhanced_Security.postman_collection.json`** ⭐ **NUEVA - COMPLETA 2025**
   - **Colección más completa con todos los endpoints faltantes**
   - **✅ Tests de MFA completos:** Setup, verify, disable
   - **✅ Tests de funcionalidades de admin:** GET /auth/users, audit logs
   - **✅ Tests de endpoints faltantes:** /auth/me, change-password, búsqueda por email
   - **✅ Flujo automatizado completo** con limpieza de datos
   - **✅ Scripts inteligentes** para generar datos únicos
   - **✅ Validaciones exhaustivas** de seguridad y autorización

2. **`Admin_Events_Complete_API.postman_collection.json`** ⭐ **RECOMENDADA - ESTABLE**
   - Colección completa y actualizada con funcionalidades básicas
   - Tests automatizados alineados con la implementación actual
   - Incluye pruebas de seguridad, validaciones y CRUD completo
   - Scripts de pre-request para generar datos únicos
   - Validaciones exhaustivas de respuestas y headers

3. **`Admin_Events_Security_Tests.postman_collection.json`** 🛡️ **ESPECIALIZADA**
   - Colección especializada en pruebas de seguridad avanzadas
   - Tests de validación de contraseñas robustas
   - Verificación de headers de seguridad (XSS, CSRF, HSTS, CSP)
   - Pruebas de rate limiting y protección contra ataques
   - Validación de tokens JWT y autorización
   - Tests de inyección SQL y XSS (seguros para testing)

3. **`Admin_Events_Microservicio_Completo.postman_collection.json`** 📝 **LEGADO**
   - Colección original (mantener para referencia)
   - Puede contener algunos tests desactualizados

4. **`AttendeesMicroservice_Security.postman_collection.json`** 📝 **LEGADO**
   - Colección original de seguridad (mantener para referencia)

### 🌍 Environments

1. **`Admin_Events_Enhanced_Environment.postman_environment.json`** ✅ **NUEVO - COMPLETO 2025**
   - **Environment optimizado para la colección Enhanced Security**
   - **Variables para MFA testing** (mfa_username, mfa_secret, etc.)
   - **Variables para admin testing** (admin_access_token, admin_user_id, etc.)
   - **Variables para búsqueda** (search_attendee_email, search_attendee_doc)
   - **Generación automática de datos únicos**

2. **`Admin_Events_Local_Environment.postman_environment.json`** ✅ **ESTABLE**
   - Environment configurado para desarrollo local
   - Variables predefinidas para pruebas rápidas
   - Incluye credenciales de administrador predeterminadas
   - Variables para generar datos únicos

## 🆕 **NUEVOS TESTS IMPLEMENTADOS (2025)**

### 🔐 **Tests de MFA (Multi-Factor Authentication)**
- ✅ **Setup MFA:** Configuración inicial de 2FA con secret y QR code
- ✅ **Verify MFA:** Verificación de códigos TOTP (con manejo de códigos de prueba)
- ✅ **Disable MFA:** Deshabilitación de autenticación de dos factores
- ✅ **Tests de seguridad:** Acceso sin autenticación a endpoints MFA

### 👨‍💼 **Tests de Funcionalidades de Administrador**
- ✅ **GET /auth/users:** Lista completa de usuarios (solo admins)
- ✅ **GET /auth/audit-logs:** Logs de auditoría con filtros
- ✅ **Autorización:** Verificación que usuarios regulares no accedan
- ✅ **Validaciones:** Estructura de datos y propiedades requeridas

### 👤 **Tests de Endpoints Faltantes**
- ✅ **GET /auth/me:** Perfil del usuario autenticado
- ✅ **POST /auth/change-password:** Cambio de contraseña con validaciones
- ✅ **GET /attendees/search/by-email/{email}:** Búsqueda de asistentes por email
- ✅ **Tests de seguridad:** Acceso sin autenticación a endpoints protegidos

### 🧪 **Flujo de Testing Automatizado**
1. **Configuración inicial:** Creación automática de admin y usuario MFA
2. **Tests de MFA:** Flujo completo de configuración y uso
3. **Tests de admin:** Verificación de funcionalidades administrativas
4. **Tests de endpoints:** Validación de nuevos endpoints
5. **Limpieza:** Eliminación automática de datos de prueba

### 📊 **Mejoras en Validaciones**
- **Estructura de respuestas:** Validación exhaustiva de propiedades JSON
- **Headers de seguridad:** Verificación de headers en todas las respuestas
- **Autorización granular:** Tests específicos por scope y rol
- **Datos sensibles:** Verificación que no se expongan passwords/secrets
- **Rate limiting:** Validación de límites y headers de control

## 🚀 Cómo Usar

### 1. Importar en Postman

1. Abre Postman
2. Click en "Import"
3. Arrastra los archivos JSON o selecciona "Upload Files"
4. **Importa prioritariamente:**
   - `Admin_Events_Enhanced_Security.postman_collection.json` ⭐ **NUEVA - MÁS COMPLETA**
   - `Admin_Events_Enhanced_Environment.postman_environment.json` ⭐ **NUEVO ENVIRONMENT**
   - `Admin_Events_Complete_API.postman_collection.json` (alternativa estable)
   - `Admin_Events_Security_Tests.postman_collection.json` (pruebas especializadas)

### 2. Configurar Environment

1. **Para la colección Enhanced Security (RECOMENDADO):**
   - Selecciona el environment `Admin_Events_Enhanced_Environment`
   - **Variables principales:**
     - `base_url`: `http://localhost:3000` (ajustar si usas otro puerto)
     - `test_password`: Contraseña segura por defecto
     - **Variables automáticas:** Los scripts generarán automáticamente usernames, emails y tokens únicos

2. **Para colecciones estables:**
   - Selecciona el environment `Admin_Events_Local_Environment`
   - Verifica que las variables estén configuradas:
     - `base_url`: `http://localhost:3000`
     - `admin_username`: `admin`
     - `admin_password`: `Admin123!`
     - `test_password`: `TestPass123!`

### 3. Configuración para Tests de MFA

**⚠️ Importante para tests de MFA reales:**

1. **Variable `MFA_ENABLED=true`** en el archivo `config.py` de la API
2. **Para tests automatizados:** Los tests usan códigos simulados y manejan errores esperados
3. **Para tests manuales:** 
   - Ejecuta "Setup MFA" y copia el `secret` del response
   - Usa una app como Google Authenticator/Authy para generar códigos reales
   - Reemplaza `test_mfa_code` en el environment con el código generado

### 3. Asegurar que el Servidor Esté Funcionando

```bash
# Navegar al directorio del proyecto
cd admin_events_upgrade/admin_events_attendees

# Iniciar el servidor
./run.sh
```

O alternativamente:
```bash
PYTHONPATH=.venv/lib/python3.12/site-packages python3 main.py
```

### 4. Ejecutar Pruebas

#### 🆕 **Flujo Enhanced Security (RECOMENDADO - 2025)**
1. **Selecciona:** `Admin_Events_Enhanced_Security` collection
2. **Environment:** `Admin_Events_Enhanced_Environment`
3. **Ejecuta las carpetas en orden:**
   - 🔧 **Configuración Inicial** - Crea usuarios admin y MFA automáticamente
   - 🔐 **Tests de MFA** - Flujo completo de autenticación de dos factores  
   - 👨‍💼 **Tests de Admin** - Funcionalidades administrativas y autorización
   - 👤 **Endpoints Faltantes** - Perfil, cambio contraseña, búsqueda por email
   - 🔍 **Búsqueda Faltantes** - Tests de búsqueda por email con datos de prueba
   - 🧹 **Limpieza** - Eliminación automática de datos de prueba

#### 🔄 Ejecución Manual (Recomendado para Desarrollo)
1. Ejecuta las requests una por una siguiendo el orden de las carpetas
2. Observa los tests automatizados en la pestaña "Test Results"

#### 📊 **Interpretación de Resultados Enhanced Security**

**✅ Tests Exitosos Esperados:**
- Todos los tests de configuración inicial
- Tests de funcionalidades de admin con token de admin
- Tests de perfil y cambio de contraseña con autenticación
- Tests de búsqueda con datos válidos

**❌ Errores Esperados (Tests Negativos):**
- MFA verification con código de prueba (401)
- Acceso a funciones admin sin privilegios (403)
- Acceso sin autenticación (401)
- Búsqueda con emails inexistentes (resultados vacíos)

1. **Ejecutar Flujo Completo Recomendado (API Completa):**
   - Selecciona la colección `Admin_Events_Complete_API`
   - Ejecuta las carpetas en orden:
     1. 🏥 Health & Status
     2. 🔐 Autenticación y Seguridad (incluye Login de Admin)
     3. 👥 Gestión de Asistentes
     4. 📋 Validaciones de Datos

2. **Ejecutar Pruebas de Seguridad Especializadas:**
   - Selecciona la colección `Admin_Events_Security_Tests`

3. **Ejecutar Pruebas de Búsquedas Específicas:**
   - Selecciona la colección `Admin_Events_Search_Endpoints`
   - Primero asegúrate de tener un token válido (ejecuta Login desde la colección principal)
   - Ejecuta las búsquedas por documento y email

## 🔍 Endpoints de Búsqueda
(Disponibles en la colección principal y en la colección adicional de búsquedas)

### Buscar por parámetros generales
- `GET /attendees/search?email=test@example.com`
- `GET /attendees/search?first_name=Juan`
- `GET /attendees/search?last_name=Pérez`
- `GET /attendees/search?document_number=12345678`

### Buscar por documento específico
- `GET /attendees/search/by-document/{document_type}/{document_number}`
- Ejemplo: `/attendees/search/by-document/DNI/12345678`
- Retorna un único asistente (404 si no existe)

### Buscar por email
- `GET /attendees/search/by-email/{email}`
- Busca asistentes que contengan el email especificado
- Ejemplo: `/attendees/search/by-email/gmail.com`
- Retorna array de asistentes coincidentes
   - Ejecuta primero el Login de Admin en la colección principal
   - Luego ejecuta todas las pruebas de seguridad

#### ⚡ Ejecución Automática Completa
1. Click en la colección deseada
2. Click en "Run collection" 
3. Asegúrate de que el environment "Admin Events - Local Environment" esté seleccionado
4. Click en "Run [Nombre de la Colección]"
5. Observa los resultados en tiempo real

## 📋 Flujo de Pruebas Incluido

### 🏥 1. Health & Status
- ✅ **Health Check** del sistema con verificación de headers de seguridad
- ✅ **API Root Info** con información de características

### 🔐 2. Autenticación y Seguridad
- ❌ **Registro con contraseña débil** (Error esperado - validación de 8+ caracteres)
- ✅ **Registro exitoso** con contraseña segura y generación de datos únicos
- ❌ **Login con credenciales incorrectas** (Error esperado)  
- ✅ **Login exitoso** de usuario normal y obtención de tokens JWT
- ✅ **Login de administrador** con credenciales predeterminadas
- ❌ **Acceso con token inválido** (Error esperado)

### 👥 3. Gestión de Asistentes (Requiere Autenticación)
- ❌ **Acceso sin autenticación** (Error esperado - 401)
- ✅ **Listar asistentes** con autenticación válida
- ❌ **Crear asistente con datos inválidos** (Error esperado - enum inválido)
- ✅ **Crear asistente** con datos válidos y únicos
- ✅ **Obtener asistente por ID** específico
- ✅ **Actualizar asistente** existente
- ✅ **Eliminar asistente** completamente

### 📋 4. Validaciones de Datos
- ❌ **Email inválido** (Error esperado - formato incorrecto)
- ❌ **Campos requeridos faltantes** (Error esperado)

### �️ 5. Pruebas de Seguridad Avanzadas (Colección Especializada)
- 🔐 **Validaciones de Contraseña:**
  - Muy corta (< 8 caracteres)
  - Sin mayúsculas
  - Sin números
- 🛡️ **Headers de Seguridad:**
  - XSS Protection
  - Content-Type-Options
  - Frame-Options
  - HSTS y CSP
- 🚦 **Rate Limiting:**
  - Verificación de headers
  - Múltiples requests rápidas
- 🔑 **Seguridad de Tokens JWT:**
  - Token malformado
  - Token vacío
  - Sin header Authorization
- 💉 **Validación de Datos:**
  - Intento de SQL Injection (seguro)
  - Intento de XSS (seguro)
  - Campos excesivamente largos

## 🧪 Tests Automatizados Incluidos

Cada request incluye tests automáticos que verifican:

### ✅ **Casos de Éxito**
- Status codes correctos (200, 201)
- Estructura de respuesta válida
- Tokens JWT presentes y válidos
- Headers de seguridad aplicados correctamente
- Datos creados/actualizados correctamente
- Headers de rate limiting presentes

### ❌ **Casos de Error**
- Status codes de error apropiados (401, 403, 422)
- Mensajes de error descriptivos y específicos
- Validaciones de datos funcionando correctamente
- Seguridad aplicada en todos los endpoints

### 🔒 **Verificaciones de Seguridad**
- Headers de seguridad presentes en todas las respuestas
- Rate limiting configurado y funcionando (100 req/min)
- Autenticación JWT obligatoria para endpoints protegidos
- Autorización basada en scopes (read:attendees, write:attendees)
- Validaciones de entrada robustas
- Tiempos de respuesta razonables
- No filtración de información del servidor

## 📊 Ejemplos de Respuestas Esperadas

### ✅ Registro Exitoso (201 Created)
```json
{
  "id": 1,
  "username": "testuser_12345",
  "email": "test_12345@test.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-07-27T06:00:00",
  "last_login": null,
  "mfa_enabled": false
}
```

### ✅ Login Exitoso (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### ✅ Asistente Creado (201 Created)
```json
{
  "name": "Juan Pérez Test",
  "email": "attendee_1753596000@test.com",
  "document_type": "DNI",
  "document_number": "17535960001234",
  "phone_number": "555-1234",
  "address": "Calle Test 123",
  "date_of_birth": null,
  "gender": null,
  "attendee_id": 1,
  "created_at": "2025-07-27T06:00:00",
  "updated_at": null
}
```

### ❌ Error de Validación (422 Unprocessable Entity)
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 8}
    }
  ]
}
```

### ❌ Error de Autenticación (401 Unauthorized)
```json
{
  "detail": "Could not validate credentials"
}
```

## 🔧 Variables de Environment Utilizadas

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `base_url` | URL base de la API | `http://localhost:3000` |
| `access_token` | Token JWT de acceso | Se establece automáticamente |
| `refresh_token` | Token de renovación | Se establece automáticamente |
| `admin_username` | Usuario administrador | `admin` |
| `admin_password` | Contraseña de admin | `Admin123!` |
| `test_username` | Usuario de prueba | Se genera dinámicamente |
| `test_email` | Email de prueba | Se genera dinámicamente |
| `test_password` | Contraseña de prueba | `TestPass123!` |
| `attendee_id` | ID de asistente creado | Se establece automáticamente |
| `unique_doc_number` | Número de documento único | Se genera dinámicamente |
| `unique_email` | Email único para asistentes | Se genera dinámicamente |

## 🚨 Notas Importantes

### ⚠️ Seguridad
- Las pruebas de seguridad están diseñadas para entornos de desarrollo/testing
- NO ejecutar pruebas de inyección en producción sin autorización
- Las credenciales por defecto deben cambiarse en producción

### 🔄 Datos Únicos
- Las colecciones utilizan scripts para generar datos únicos automáticamente
- Cada ejecución crea asistentes con datos nuevos para evitar conflictos
- Los datos se almacenan en variables de environment para ser reutilizados

### 📋 Colecciones Disponibles

#### 1. Admin_Events_Complete_API.postman_collection.json
- **Propósito**: Pruebas completas de funcionalidad de la API
- **Incluye**: CRUD completo, autenticación, validaciones, búsquedas básicas
- **Recomendado para**: Desarrollo, testing general, verificación de funcionalidad

#### 2. Admin_Events_Security_Tests.postman_collection.json
- **Propósito**: Pruebas especializadas de seguridad
- **Incluye**: Tests de inyección, validación de headers, rate limiting
- **Recomendado para**: Auditorías de seguridad, testing de penetración

#### 3. Admin_Events_Search_Endpoints.postman_collection.json
- **Propósito**: Tests específicos para endpoints de búsqueda
- **Incluye**: Búsquedas por documento, email, validaciones de auth
- **Recomendado para**: Testing de funcionalidad de búsqueda, validación de filtros

### 🔍 Tips de Uso
- Ejecuta primero la colección completa para establecer el contexto
- Las colecciones de seguridad y búsqueda requieren token válido
- Usa el Collection Runner para ejecución automatizada
- Revisa los tests en cada request para entender las validaciones
- Esto evita conflictos de duplicados al ejecutar múltiples veces
- Los emails y documentos se generan con timestamps y números aleatorios

### 📈 Monitoreo
- Todas las respuestas incluyen headers de timing (`x-process-time`)
- Los headers de rate limiting muestran límites y uso actual
- Los logs del servidor muestran todas las requests procesadas

## 🏃‍♂️ Flujo de Ejecución Recomendado

### Para Desarrollo Diario:
1. **Ejecutar Health Check** para verificar que el servidor está funcionando
2. **Login de Admin** para obtener tokens
3. **Pruebas CRUD básicas** de asistentes
4. **Verificar funcionalidades específicas** según necesidad

### Para Testing Completo:
1. **Ejecutar colección completa** `Admin_Events_Complete_API`
2. **Ejecutar pruebas de seguridad** `Admin_Events_Security_Tests`
3. **Revisar todos los tests** para asegurar 100% de éxito
4. **Verificar logs del servidor** para auditoría

### Para CI/CD:
1. **Utilizar Newman** (CLI de Postman) para automatizar
2. **Exportar resultados** en formato JSON/HTML
3. **Integrar con pipelines** de desarrollo

## 📞 Soporte

Si encuentras problemas con las colecciones:

1. **Verificar que el servidor esté funcionando**: `curl http://localhost:3000/health`
2. **Revisar variables de environment**: Especialmente `base_url` y tokens
3. **Ejecutar tests uno por uno** para identificar el punto de falla
4. **Revisar logs del servidor** en `/tmp/test_server.log`
5. **Consultar documentación de la API**: `http://localhost:3000/docs`
  "last_login": null,
  "mfa_enabled": false
}
```

### ❌ Error de Validación de Contraseña
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

### ✅ Login Exitoso
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "VPOY8mRmPWGeGPVdu-f8eX1ZB070NclNPJpfCbWMZ2w",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 🛠️ Variables de Environment

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `base_url` | URL base del API | `http://localhost:3000` |
| `access_token` | JWT token de acceso | Configurado automáticamente |
| `refresh_token` | Token de renovación | Configurado automáticamente |
| `test_username` | Usuario para pruebas | `testuser` |
| `test_email` | Email para pruebas | `test@test.com` |
| `test_password` | Contraseña segura | `TestPass123!` |
| `attendee_id` | ID del asistente creado | Configurado automáticamente |

## 🔍 Monitoreo Durante las Pruebas

### Logs del Servidor
Mientras ejecutas las pruebas, observa los logs del servidor para ver:
- Requests llegando al servidor
- Tiempos de respuesta
- Errores de autenticación
- Acciones de auditoría

### Headers de Respuesta
Las respuestas incluyen headers informativos:
- **Rate Limiting**: `X-RateLimit-*`
- **Seguridad**: `X-Content-Type-Options`, `X-Frame-Options`, etc.
- **Tiempo de Procesamiento**: `X-Process-Time`

## 🚨 Solución de Problemas

### ❌ Connection Refused
- Verificar que el servidor esté ejecutándose en puerto 3000
- Revisar que no hay firewall bloqueando el puerto

### ❌ Tests Fallando
- Verificar que el environment correcto esté seleccionado
- Asegurar que las variables estén configuradas
- Ejecutar las requests en orden secuencial

### ❌ Tokens Expirados
- Los tokens JWT expiran en 30 minutos
- Usar el endpoint de refresh token o hacer login nuevamente

---

**¡Las colecciones están listas para probar completamente el microservicio!** 🎉

Para soporte adicional, revisar:
- `GUIA_EJECUCION_COMPLETA.md` - Instrucciones detalladas
- `README_SECURITY.md` - Documentación de seguridad
- `http://localhost:3000/docs` - Documentación interactiva del API
