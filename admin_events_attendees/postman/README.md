# 📮 Colección de Postman - Admin Events Microservicio

Esta carpeta contiene las colecciones y environments de Postman para probar completamente el microservicio de gestión de asistentes con todas las funcionalidades de seguridad implementadas.

## 📁 Archivos Incluidos

### 🧪 Colecciones de Pruebas

1. **`Admin_Events_Complete_API.postman_collection.json`** ⭐ **NUEVA - RECOMENDADA**
   - Colección completa y actualizada con todas las funcionalidades
   - Tests automatizados alineados con la implementación actual
   - Incluye pruebas de seguridad, validaciones y CRUD completo
   - Scripts de pre-request para generar datos únicos
   - Validaciones exhaustivas de respuestas y headers

2. **`Admin_Events_Security_Tests.postman_collection.json`** 🛡️ **NUEVA - ESPECIALIZADA**
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

1. **`Admin_Events_Local_Environment.postman_environment.json`** ✅ **ACTUALIZADO**
   - Environment configurado para desarrollo local
   - Variables predefinidas para pruebas rápidas
   - Incluye credenciales de administrador predeterminadas
   - Variables para generar datos únicos

## 🚀 Cómo Usar

### 1. Importar en Postman

1. Abre Postman
2. Click en "Import"
3. Arrastra los archivos JSON o selecciona "Upload Files"
4. **Importa prioritariamente:**
   - `Admin_Events_Complete_API.postman_collection.json`
   - `Admin_Events_Security_Tests.postman_collection.json`
   - `Admin_Events_Local_Environment.postman_environment.json`

### 2. Configurar Environment

1. En Postman, selecciona el environment "Admin Events - Local Environment"
2. Verifica que las variables estén configuradas:
   - `base_url`: `http://localhost:3000`
   - `admin_username`: `admin`
   - `admin_password`: `Admin123!`
   - `test_password`: `TestPass123!`

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

#### 🔄 Ejecución Manual (Recomendado para Desarrollo)
1. Ejecuta las requests una por una siguiendo el orden de las carpetas
2. Observa los tests automatizados en la pestaña "Test Results"

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
