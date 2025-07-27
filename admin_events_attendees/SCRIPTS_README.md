# 🚀 Scripts de Ejecución - Admin Events

## 📋 Scripts Disponibles

### 1. 🚀 **`run.sh`** - Ejecutar Proyecto Completo

**Descripción:** Script único que configura y ejecuta todo el microservicio automáticamente.

```bash
./run.sh
```

**¿Qué hace?**
- ✅ Verifica Python 3.8+
- ✅ Crea entorno virtual (.venv)
- ✅ Instala todas las dependencias
- ✅ Configura archivo .env con variables de entorno
- ✅ Inicializa base de datos SQLite
- ✅ Crea usuario administrador automáticamente
- ✅ Inicia servidor en puerto 3000

**Credenciales creadas automáticamente:**
- **Usuario:** `admin`
- **Contraseña:** `Admin123!`

**URLs disponibles después del inicio:**
- API Base: http://localhost:3000
- Documentación: http://localhost:3000/docs
- Health Check: http://localhost:3000/health

---

### 2. 🧪 **`test.sh`** - Ejecutar Todas las Pruebas

**Descripción:** Suite completa de pruebas que verifica toda la funcionalidad y seguridad.

```bash
./test.sh
```

**¿Qué hace?**
- 🔬 **Tests unitarios** con pytest
- 🌐 **Tests de integración** de API endpoints
- 🔐 **Tests de seguridad** (autenticación, JWT, validaciones)
- 📋 **Tests de funcionalidad** (CRUD completo de asistentes)
- 🛡️ **Tests de validación** (datos, headers, rate limiting)

**Tests específicos incluidos:**
- ❌ Registro con contraseña débil (error esperado)
- ✅ Registro exitoso con contraseña segura
- ❌ Login con credenciales incorrectas (error esperado)
- ✅ Login exitoso y obtención de tokens JWT
- ❌ Acceso sin autenticación (error esperado)
- ✅ CRUD completo de asistentes
- ❌ Validaciones de datos inválidos (error esperado)
- ✅ Headers de seguridad presentes
- ✅ Rate limiting funcionando

**Salida del script:**
- Estadísticas detalladas de tests
- Conteo de tests exitosos vs fallidos
- Logs detallados para debugging
- Resumen final de funcionalidades verificadas

---

## 🎯 Flujo de Uso Recomendado

### Primera vez ejecutando el proyecto:
```bash
# 1. Ejecutar proyecto completo
./run.sh

# 2. En otra terminal, ejecutar todas las pruebas
./test.sh
```

### Ejecuciones posteriores:
```bash
# Si ya configuraste todo antes, solo iniciar servidor
./run.sh

# Ejecutar pruebas cuando hagas cambios
./test.sh
```

---

## 🔍 Detalles Técnicos

### Variables de Entorno (configuradas automáticamente)
```bash
JWT_SECRET_KEY=development-secret-key-please-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./attendees.db
BCRYPT_ROUNDS=12
DEBUG=true
HOST=0.0.0.0
PORT=3000
RATE_LIMIT_PER_MINUTE=100
MFA_ENABLED=true
MFA_ISSUER=AdminEvents
```

### Estructura de Archivos Generados
```
admin_events_attendees/
├── .venv/                 # Entorno virtual (creado automáticamente)
├── .env                   # Variables de entorno (creado automáticamente)
├── attendees.db           # Base de datos SQLite (creado automáticamente)
├── run.sh                 # Script de ejecución principal
├── test.sh                # Script de pruebas completas
└── requirements.txt       # Dependencias (existente)
```

---

## 🚨 Solución de Problemas

### ❌ **Error: "Python 3 no está instalado"**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# macOS
brew install python3
```

### ❌ **Error: "Puerto 3000 ya está en uso"**
El script automáticamente:
1. Detecta si el puerto está en uso
2. Intenta detener procesos existentes
3. Inicia el nuevo servidor

### ❌ **Error: "No se pudo crear el entorno virtual"**
```bash
# Verificar permisos de escritura
ls -la .
chmod 755 .

# Verificar python3-venv instalado
sudo apt install python3-venv  # Ubuntu/Debian
```

### ❌ **Tests fallando**
```bash
# Ver logs detallados
cat /tmp/pytest_output.log     # Tests unitarios
cat /tmp/test_server.log       # Logs del servidor de testing

# Verificar que el servidor esté funcionando
curl http://localhost:3000/health
```

---

## 📈 Métricas de Éxito

### ✅ **Script `run.sh` exitoso cuando:**
- Servidor inicia sin errores
- Base de datos se crea correctamente
- Usuario admin se crea/existe
- Puerto 3000 responde
- URLs principales accesibles

### ✅ **Script `test.sh` exitoso cuando:**
- Todos los tests unitarios pasan
- Tests de integración funcionan
- Validaciones de seguridad activas
- CRUD completo funcional
- Rate limiting activo
- Headers de seguridad presentes

---

**¡Los scripts están optimizados para facilitar el desarrollo y testing del microservicio!** 🎉
