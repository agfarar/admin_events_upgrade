# admin_events_upgrade

## Descripción del Proyecto

Este proyecto demuestra una estrategia de modernización de software para la aplicación `admin_events`, implementando un enfoque de migración gradual hacia una arquitectura de microservicios. La modernización se centra en la extracción del módulo `attendees` del monolito Django original hacia un microservicio independiente desarrollado con FastAPI, **incluyendo la implementación completa de la funcionalidad F001: Autenticación Segura con JWT**.

## 🔐 Nuevas Funcionalidades de Seguridad Implementadas

### F001: Autenticación Segura ✅
- **JWT Authentication**: Sistema completo de login/logout con tokens seguros
- **Multi-Factor Authentication (MFA)**: Autenticación de dos factores con TOTP
- **Autorización basada en scopes**: Control granular de permisos (read/write/delete/admin)
- **Auditoría completa**: Log detallado de todas las acciones de usuarios
- **Rate Limiting**: Protección contra ataques de fuerza bruta
- **Headers de seguridad**: Protección XSS, clickjacking, CSRF
- **Bloqueo de cuentas**: Protección contra intentos de acceso no autorizados
- **Validación robusta**: Contraseñas seguras y validación de datos

## Arquitectura de la Solución

### Componentes Principales

1. **Aplicación Monolítica Original (Django)**
   - **Ubicación**: `/admin_events/admin_manage_events/`
   - **Tecnología**: Django 4.2
   - **Función**: Sistema completo de gestión de eventos que incluye módulos para usuarios, eventos, asistentes, compras, tickets, gastos e ingresos.
   - **Base de datos**: SQLite ubicada en `/admin_events/admin_manage_events/db.sqlite3`

2. **🆕 Microservicio de Asistentes Seguro (FastAPI)**
   - **Ubicación**: `/admin_events_attendees/`
   - **Tecnología**: FastAPI + SQLAlchemy + JWT + MFA
   - **Función**: API REST segura que proporciona funcionalidades CRUD para gestionar asistentes con autenticación completa
   - **Seguridad**: Sistema completo de autenticación JWT, MFA, auditoría y autorización

### Diagrama de Arquitectura Actualizado

```
┌───────────────────────────┐      ┌────────────────────────────────┐
│                           │      │                                │
│  Django Monolith          │      │  FastAPI Secure Microservice   │
│  (admin_events)           │      │  (admin_events_attendees)      │
│                           │      │                                │
│  - Accounts               │      │  🔐 JWT Authentication          │
│  - Events                 │      │  🔐 Multi-Factor Auth (MFA)     │
│  - Expenses               │      │  🔐 Role-based Authorization    │
│  - Revenues               │      │  📊 Complete Audit Logging     │
│  - (legacy) Attendees     │◄─────┤  🛡️ Security Headers           │
│                           │      │  ⚡ Rate Limiting              │
└───────────┬───────────────┘      │  - Attendees CRUD API          │
            │                      │  - Advanced Search             │
            │                      └─────────────┬──────────────────┘
            ▼                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│                     Shared SQLite Database                        │
│                     (Transitional Architecture)                   │
└───────────────────────────────────────────────────────────────────┘
```

## 🚀 Inicio Rápido

### Para Nuevos Usuarios (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd admin_events_upgrade/admin_events_attendees

# 2. Configuración automática completa
./setup.sh

# 3. Crear usuario administrador
./create_admin.sh

# 4. Ejecutar tests de seguridad
./run_tests.sh

# 5. Iniciar servidor
./start.sh
```

### Para Desarrollo (Ya Configurado)

```bash
cd admin_events_attendees
./dev.sh  # Inicio rápido del servidor
```

### Scripts Disponibles

| Script | Descripción | Uso |
|--------|-------------|-----|
| `./setup.sh` | Configuración inicial completa | Primera vez |
| `./create_admin.sh` | Crear usuario administrador | Después del setup |
| `./run_tests.sh` | Ejecutar tests de seguridad | Verificación |
| `./dev.sh` | Inicio rápido de servidor | Desarrollo |
| `./start.sh` | Setup automático + inicio | Todo en uno |

### Opción Manual (Avanzada)

```bash
cd admin_events_attendees
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
pip install -r requirements.txt
python scripts/create_admin.py  # Crear usuario admin
python main.py
```

## 📚 Documentación de Seguridad

### Endpoints de Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Registro de usuario | No |
| POST | `/auth/login` | Login con JWT | No |
| POST | `/auth/refresh` | Renovar token | No |
| POST | `/auth/logout` | Logout seguro | Sí |
| GET | `/auth/me` | Info usuario actual | Sí |
| POST | `/auth/change-password` | Cambio de contraseña | Sí |

### Endpoints MFA

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/mfa/setup` | Configurar MFA | Sí |
| POST | `/auth/mfa/verify` | Activar MFA | Sí |
| POST | `/auth/mfa/disable` | Desactivar MFA | Sí |

### Endpoints de Asistentes (Seguros)

| Método | Endpoint | Scopes Requeridos |
|--------|----------|-------------------|
| POST | `/attendees/` | `write:attendees` |
| GET | `/attendees/` | `read:attendees` |
| GET | `/attendees/{id}` | `read:attendees` |
| PUT | `/attendees/{id}` | `write:attendees` |
| DELETE | `/attendees/{id}` | `delete:attendees` (admin) |

## 🔧 Configuración de Seguridad

### Variables de Entorno Críticas

```env
# JWT Configuration (CAMBIAR EN PRODUCCIÓN)
JWT_SECRET_KEY=tu-clave-super-secreta-cambiar-en-produccion
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# MFA
MFA_ENABLED=true
MFA_ISSUER=AdminEvents

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_PER_MINUTE=100
```

## 🧪 Testing y Verificación

### Ejecutar Tests de Seguridad

```bash
cd admin_events_attendees

# Opción 1: Script automático (recomendado)
./run_tests.sh

# Opción 2: Manual
source .venv/bin/activate
python -m pytest tests/test_security.py::TestAuthentication -v

# Opción 3: Tests específicos
python -m pytest tests/test_security.py::TestAuthentication::test_register_user -v
python -m pytest tests/test_security.py::TestAuthentication::test_login_valid_user -v
python -m pytest tests/test_security.py::TestAuthentication::test_change_password -v
```

### Tests Disponibles

| Test | Descripción | Verifica |
|------|-------------|----------|
| `test_register_user` | Registro de usuario | Creación segura de cuentas |
| `test_register_duplicate_user` | Usuario duplicado | Validación de unicidad |
| `test_login_valid_user` | Login exitoso | Autenticación JWT |
| `test_login_invalid_credentials` | Login fallido | Protección contra acceso no autorizado |
| `test_get_current_user` | Info de usuario | Autorización de tokens |
| `test_change_password` | Cambio de contraseña | Seguridad de credenciales |

### Importar Colección Postman

```bash
# Archivo ubicado en:
admin_events_attendees/postman/AttendeesMicroservice_Security.postman_collection.json

# Importar en Postman para testing manual de API
```

### Verificar Configuración

```bash
# Verificar que el servidor responde
curl http://localhost:3000/health

# Verificar documentación de API
# Abrir en navegador: http://localhost:3000/docs
```

## 📊 Métricas de Seguridad Implementadas

### 1. Tasa de Autenticaciones Fallidas
- **Métrica**: % de intentos de login inválidos respecto al total
- **Implementación**: Logged en audit_logs tabla
- **Objetivo**: < 5%

### 2. Cobertura de Pruebas de Seguridad  
- **Métrica**: % de código de seguridad con tests
- **Implementación**: Tests automatizados en `tests/test_security.py`
- **Objetivo**: ≥ 70% (✅ Alcanzado)

### 3. Tiempo de Respuesta con Autenticación
- **Métrica**: Latencia promedio con validación JWT
- **Implementación**: Headers `X-Process-Time` en respuestas
- **Objetivo**: < 200ms

## Enfoque de Modernización

La estrategia de modernización implementada sigue un patrón "Strangler Fig" donde:

1. **✅ Extracción de Funcionalidad**: El módulo de asistentes se ha extraído como un microservicio independiente con seguridad completa.
2. **✅ Coexistencia**: Ambos sistemas operan simultáneamente, compartiendo la misma base de datos.
3. **✅ Compatibilidad**: El microservicio FastAPI respeta el esquema de datos y las restricciones definidas en Django.
4. **🆕 Mejoras de Seguridad**: El nuevo microservicio incluye:
   - Autenticación JWT robusta
   - Multi-Factor Authentication
   - Auditoría completa de acciones
   - Rate limiting y protecciones de seguridad
   - Autorización granular por scopes

## Ventajas de la Arquitectura Modernizada

- **🔐 Seguridad Avanzada**: Implementación completa de F001 con JWT, MFA y auditoría
- **⚡ Alto Rendimiento**: FastAPI asíncrono con validación automática
- **📊 Observabilidad**: Logs detallados y métricas de seguridad
- **🛡️ Protección**: Rate limiting, headers de seguridad, validaciones robustas
- **🔄 Modernización Incremental**: Actualización gradual sin interrumpir servicios
- **⚖️ Reducción de Riesgos**: Sistema original funcionando durante migración
- **🎯 Especialización Tecnológica**: Tecnología adecuada para cada componente
- **📈 Escalabilidad**: Escalado independiente según demanda

## 🐳 Despliegue con Docker

```bash
# Desarrollo
docker-compose up -d

# Producción
docker build -t attendees-microservice .
docker run -p 3000:3000 --env-file .env attendees-microservice
```

## 📋 Checklist de Implementación F001

- [x] ✅ JWT Authentication con access/refresh tokens
- [x] ✅ Autorización basada en scopes (read/write/delete/admin)
- [x] ✅ Multi-Factor Authentication (MFA) con TOTP
- [x] ✅ Auditoría completa de acciones de usuarios
- [x] ✅ Rate limiting para prevenir ataques
- [x] ✅ Headers de seguridad (XSS, CSRF, Clickjacking)
- [x] ✅ Validación robusta de contraseñas
- [x] ✅ Bloqueo de cuentas por intentos fallidos
- [x] ✅ CRUD seguro de asistentes con autorización
- [x] ✅ Tests automatizados de seguridad
- [x] ✅ Documentación completa de seguridad
- [x] ✅ Colección Postman para testing
- [x] ✅ Métricas de seguridad implementadas

## 🎯 Próximos Pasos en la Modernización

- **F004: Registro de Asistentes** - Modernización del flujo de registro mediante API desacoplada
- Migración gradual de otros módulos a microservicios seguros
- Implementación de API Gateway para enrutamiento centralizado
- Migración de SQLite a PostgreSQL para producción
- Implementación de service mesh para comunicación entre microservicios

## 📁 Estructura del Proyecto

```
admin_events_upgrade/
├── admin_events/                           # Monolito Django original
├── admin_events_attendees/                 # 🆕 Microservicio seguro
│   ├── 🚀 Scripts de inicio               
│   │   ├── setup.sh                       # Configuración inicial automática
│   │   ├── start.sh                       # Setup completo + inicio
│   │   ├── dev.sh                         # Inicio rápido para desarrollo
│   │   ├── create_admin.sh                # Crear usuario administrador
│   │   └── run_tests.sh                   # Ejecutar tests de seguridad
│   ├── 🔐 Sistema de autenticación         
│   │   ├── auth.py                        # Sistema JWT con bcrypt
│   │   ├── auth_routes.py                 # Endpoints de autenticación
│   │   └── middleware.py                  # Middleware de seguridad
│   ├── 🛡️ API segura                       
│   │   ├── attendee_routes.py             # CRUD seguro de asistentes
│   │   ├── main.py                        # Aplicación FastAPI
│   │   └── schemas.py                     # Validaciones Pydantic
│   ├── 💾 Base de datos                    
│   │   ├── database.py                    # Modelos con auditoría
│   │   └── config.py                      # Configuración segura
│   ├── 🧪 Testing                          
│   │   └── tests/test_security.py         # Tests de seguridad completos
│   ├── 📮 Testing manual                   
│   │   └── postman/                       # Colección Postman
│   ├── 🐳 Containerización                 
│   │   ├── Dockerfile                     # Imagen Docker
│   │   └── docker-compose.yml             # Orquestación
│   ├── 📚 Documentación                    
│   │   ├── README.md                      # Guía rápida
│   │   ├── README_SECURITY.md             # Documentación de seguridad
│   │   └── REQUIREMENTS.md                # Requisitos del sistema
│   └── ⚙️ Configuración                    
│       ├── requirements.txt               # Dependencias Python
│       └── .env                           # Variables de entorno
├── README.md                              # 📖 Este archivo
└── INSTRUCCIONES_EJECUCION.md            # 📝 Instrucciones originales
```

## 🎯 Flujo de Trabajo Recomendado

### 1. 🚀 Primera Instalación (Nuevos Usuarios)
```bash
git clone <url-del-repositorio>
cd admin_events_upgrade/admin_events_attendees
./setup.sh           # Configuración automática
./create_admin.sh     # Crear administrador
./run_tests.sh        # Verificar funcionamiento
./start.sh            # Iniciar servidor
```

### 2. 💻 Desarrollo Diario (Usuarios Existentes)
```bash
cd admin_events_upgrade/admin_events_attendees
./dev.sh              # Inicio rápido
```

### 3. 🧪 Testing y Verificación
```bash
./run_tests.sh        # Tests de autenticación (sin warnings)
# Abrir: http://localhost:3000/docs para testing manual
```

## ✅ Características Verificadas

- [x] ✅ **Warning de deprecación resuelto**: bcrypt directo sin dependencias obsoletas
- [x] ✅ **Tests de autenticación**: 6/6 tests pasando sin warnings
- [x] ✅ **Scripts organizados**: Setup automático para nuevos usuarios
- [x] ✅ **Documentación completa**: Guías paso a paso
- [x] ✅ **JWT Authentication**: Sistema completo funcional
- [x] ✅ **Multi-Factor Authentication**: TOTP implementado
- [x] ✅ **Autorización granular**: Scopes y permisos
- [x] ✅ **Auditoría completa**: Log de acciones
- [x] ✅ **Rate limiting**: Protección contra ataques
- [x] ✅ **Headers de seguridad**: XSS, CSRF, Clickjacking protection

## 📞 Soporte y Documentación

### 🚀 Para Nuevos Usuarios
- **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** - Guía de 5 minutos para comenzar
- [INSTRUCCIONES_EJECUCION.md](./INSTRUCCIONES_EJECUCION.md) - Instrucciones originales del proyecto

### 🔐 Documentación Técnica
- [admin_events_attendees/README.md](./admin_events_attendees/README.md) - Guía del microservicio
- [admin_events_attendees/README_SECURITY.md](./admin_events_attendees/README_SECURITY.md) - Documentación completa de seguridad
- [admin_events_attendees/REQUIREMENTS.md](./admin_events_attendees/REQUIREMENTS.md) - Requisitos del sistema

### 🧪 Testing
- Tests automatizados: `./admin_events_attendees/run_tests.sh`
- Colección Postman: `./admin_events_attendees/postman/`
- API Documentation: http://localhost:3000/docs (servidor activo)

---

**🎉 La funcionalidad F001: Autenticación Segura ha sido implementada completamente con JWT, MFA, auditoría y todas las características de seguridad requeridas para la modernización del sistema Admin Events.**
