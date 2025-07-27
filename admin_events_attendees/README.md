# Admin Events - Microservicio de Asistentes 🚀

Microservicio seguro para gestión de asistentes con autenticación JWT, MFA y auditoría completa.

## 🚀 Inicio Rápido

### Para nuevos usuarios (primera vez):

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd admin_events_upgrade/admin_events_attendees

# 2. Configuración inicial automática
./setup.sh

# 3. Crear usuario administrador
./create_admin.sh

# 4. Ejecutar tests (opcional)
./run_tests.sh

# 5. Iniciar servidor
./start.sh
```

### Para desarrollo (ya configurado):

```bash
# Inicio rápido de servidor
./dev.sh
```

## 📋 Scripts Disponibles

| Script | Descripción | Cuándo usar |
|--------|-------------|-------------|
| `./setup.sh` | Configuración inicial completa | Primera vez o reinstalación |
| `./create_admin.sh` | Crear usuario administrador | Después del setup inicial |
| `./run_tests.sh` | Ejecutar todos los tests | Desarrollo y verificación |
| `./dev.sh` | Inicio rápido de servidor | Desarrollo diario |
| `./start.sh` | Configuración + inicio | Setup automático completo |

## 🔐 Características de Seguridad

- ✅ **JWT Authentication**: Tokens seguros con renovación automática
- ✅ **Multi-Factor Authentication (MFA)**: Autenticación de dos factores
- ✅ **Autorización por Scopes**: Control granular de permisos
- ✅ **Auditoría Completa**: Log de todas las acciones
- ✅ **Rate Limiting**: Protección contra ataques
- ✅ **Headers de Seguridad**: XSS, CSRF, Clickjacking protection

## 🧪 Ejecutar Tests

```bash
# Tests completos de seguridad
./run_tests.sh

# O manualmente:
source .venv/bin/activate
python -m pytest tests/test_security.py::TestAuthentication -v
```

## 📊 Endpoints Principales

### Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Login con JWT
- `POST /auth/refresh` - Renovar token
- `GET /auth/me` - Info del usuario actual

### Asistentes (Requiere autenticación)
- `GET /attendees/` - Listar asistentes
- `POST /attendees/` - Crear asistente
- `GET /attendees/{id}` - Obtener asistente
- `PUT /attendees/{id}` - Actualizar asistente
- `DELETE /attendees/{id}` - Eliminar asistente (admin)

## 📚 Documentación

- **API Docs**: http://localhost:3000/docs (cuando el servidor esté corriendo)
- **Seguridad**: [README_SECURITY.md](./README_SECURITY.md)
- **Postman**: [postman/AttendeesMicroservice_Security.postman_collection.json](./postman/)

## ⚙️ Configuración

El archivo `.env` se crea automáticamente con valores por defecto. Para producción, cambiar:

```env
JWT_SECRET_KEY=tu-clave-super-secreta-de-produccion
DEBUG=false
```

## 🐳 Docker (Opcional)

```bash
# Desarrollo
docker-compose up -d

# Producción
docker build -t attendees-api .
docker run -p 3000:3000 --env-file .env attendees-api
```

## 🔧 Troubleshooting

### Error: "Python 3 no está instalado"
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### Error: "Entorno virtual no encontrado"
```bash
./setup.sh  # Ejecutar configuración inicial
```

### Error: "Base de datos no encontrada"
```bash
source .venv/bin/activate
python -c "from database import create_tables; create_tables()"
```

**🎯 Objetivo**: Microservicio moderno y seguro para gestión de asistentes con autenticación completa JWT y MFA.
