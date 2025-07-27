#!/bin/bash

# 🚀 Admin Events - Ejecutar Proyecto Completo
# Script único para configurar y ejecutar todo el microservicio

# Cambiar al directorio donde está el script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Admin Events - Microservicio de Asistentes Seguro"
echo "===================================================="
echo "📁 Directorio de trabajo: $SCRIPT_DIR"
echo ""

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_step() {
    echo -e "${PURPLE}🔧${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ] || [ ! -f "main.py" ]; then
    print_error "Este script debe ejecutarse desde el directorio admin_events_attendees"
    print_error "Archivos requeridos no encontrados: requirements.txt, main.py"
    exit 1
fi

# Verificar Python
print_step "Verificando Python 3.8+..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_status "Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    print_error "pip no está instalado"
    exit 1
fi

# Crear/verificar entorno virtual
print_step "Configurando entorno virtual..."
if [ ! -d ".venv" ]; then
    print_info "Creando entorno virtual..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        print_status "Entorno virtual creado"
    else
        print_error "No se pudo crear el entorno virtual"
        exit 1
    fi
else
    print_status "Entorno virtual existente encontrado"
fi

# Instalar/actualizar dependencias
print_step "Instalando dependencias..."
# Obtener la versión exacta de Python para el PYTHONPATH
PYTHON_VERSION_FULL=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
export PYTHONPATH=".venv/lib/python${PYTHON_VERSION_FULL}/site-packages"
.venv/bin/pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_status "Dependencias instaladas correctamente"
else
    print_error "Error instalando dependencias"
    exit 1
fi

# Crear archivo .env si no existe
print_step "Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    print_info "Creando archivo .env..."
    cat > .env << EOL
# JWT Configuration
JWT_SECRET_KEY=development-secret-key-please-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Database Configuration
DATABASE_URL=sqlite:///./attendees.db

# Security
BCRYPT_ROUNDS=12

# Application
DEBUG=true
HOST=0.0.0.0
PORT=3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# MFA (Multi-Factor Authentication)
MFA_ENABLED=true
MFA_ISSUER=AdminEvents
EOL
    print_status "Archivo .env creado"
else
    print_status "Archivo .env existente"
fi

# Inicializar base de datos
print_step "Inicializando base de datos..."
PYTHON_VERSION_FULL=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
export PYTHONPATH=".venv/lib/python${PYTHON_VERSION_FULL}/site-packages"
python3 -c "
from database import create_tables
create_tables()
print('✅ Base de datos inicializada')
"
if [ $? -eq 0 ]; then
    print_status "Base de datos lista"
else
    print_error "Error inicializando base de datos"
    exit 1
fi

# Crear usuario admin automáticamente
print_step "Configurando usuario administrador..."
PYTHON_VERSION_FULL=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
export PYTHONPATH=".venv/lib/python${PYTHON_VERSION_FULL}/site-packages"
python3 create_auto_admin.py
if [ $? -eq 0 ]; then
    print_status "Usuario administrador configurado"
else
    print_warning "Usando configuración existente de usuario administrador"
fi

# Verificar que el puerto no esté en uso
print_step "Verificando puerto 3000..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "Puerto 3000 ya está en uso"
    print_info "Intentando detener proceso existente..."
    pkill -f "python.*main.py" 2>/dev/null || true
    sleep 2
fi

echo ""
print_status "🎉 Configuración completada exitosamente!"
echo ""
echo -e "${CYAN}📋 Información del servicio:${NC}"
echo "   🌐 URL Base: http://localhost:3000"
echo "   📚 Documentación: http://localhost:3000/docs"
echo "   🏥 Health Check: http://localhost:3000/health"
echo ""
echo -e "${CYAN}🔐 Credenciales de administrador:${NC}"
echo "   👤 Usuario: admin"
echo "   🔑 Contraseña: Admin123!"
echo ""
echo -e "${CYAN}🛠️ Características habilitadas:${NC}"
echo "   ✅ Autenticación JWT"
echo "   ✅ Validaciones de seguridad"
echo "   ✅ Rate limiting"
echo "   ✅ Headers de seguridad"
echo "   ✅ Auditoría de acciones"
echo ""
echo -e "${YELLOW}🚀 Iniciando servidor...${NC}"
echo -e "${YELLOW}   (Presiona Ctrl+C para detener)${NC}"
echo ""

# Iniciar el servidor
PYTHON_VERSION_FULL=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
export PYTHONPATH=".venv/lib/python${PYTHON_VERSION_FULL}/site-packages"
python3 main.py
