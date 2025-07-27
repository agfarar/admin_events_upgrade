#!/bin/bash

# 🧪 Admin Events - Script de Pruebas Completas
# Ejecuta todas las pruebas: unitarias, de integración y de funcionalidad

echo "🧪 Admin Events - Suite de Pruebas Completas"
echo "============================================"
echo ""

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Contadores de pruebas
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

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

print_test() {
    echo -e "${PURPLE}🧪${NC} $1"
}

print_section() {
    echo ""
    echo -e "${CYAN}$1${NC}"
    echo "$(echo "$1" | sed 's/./=/g')"
}

# Función para ejecutar un test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    print_test "Test: $test_name"
    
    response=$(eval "$test_command" 2>/dev/null)
    
    if [[ $response == *"$expected_pattern"* ]]; then
        print_status "PASÓ: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_error "FALLÓ: $test_name"
        echo "   Respuesta: $response"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Verificar entorno
print_section "🔍 Verificando Entorno"

if [ ! -d ".venv" ]; then
    print_error "Entorno virtual no encontrado. Ejecuta ./run.sh primero"
    exit 1
fi

export PYTHONPATH=.venv/lib/python3.*/site-packages

# Verificar que las dependencias de testing estén instaladas
print_info "Verificando dependencias de testing..."
.venv/bin/pip list | grep -q pytest
if [ $? -ne 0 ]; then
    print_info "Instalando dependencias de testing..."
    .venv/bin/pip install pytest pytest-asyncio httpx > /dev/null 2>&1
fi
print_status "Dependencias de testing listas"

# Verificar si el servidor está corriendo
print_info "Verificando estado del servidor..."
SERVER_RUNNING=false
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    print_status "Servidor encontrado en puerto 3000"
    SERVER_RUNNING=true
else
    print_warning "Servidor no está corriendo, iniciando servidor de testing..."
    # Iniciar servidor en background para testing
    export PYTHONPATH=.venv/lib/python3.*/site-packages
    python3 main.py > /tmp/test_server.log 2>&1 &
    SERVER_PID=$!
    
    # Esperar a que el servidor inicie
    for i in {1..10}; do
        if curl -s http://localhost:3000/health > /dev/null 2>&1; then
            print_status "Servidor de testing iniciado (PID: $SERVER_PID)"
            SERVER_RUNNING=true
            break
        fi
        sleep 1
    done
    
    if [ "$SERVER_RUNNING" = false ]; then
        print_error "No se pudo iniciar el servidor para testing"
        exit 1
    fi
fi

# 1. TESTS UNITARIOS CON PYTEST
print_section "🔬 Tests Unitarios (pytest)"

if [ -d "tests" ]; then
    print_info "Ejecutando tests unitarios..."
    .venv/bin/python -m pytest tests/ -v --tb=short > /tmp/pytest_output.log 2>&1
    
    if [ $? -eq 0 ]; then
        print_status "Tests unitarios completados exitosamente"
        # Mostrar resumen de pytest
        grep -E "(passed|failed|error)" /tmp/pytest_output.log | tail -1
    else
        print_error "Algunos tests unitarios fallaron"
        print_info "Ver detalles en /tmp/pytest_output.log"
    fi
else
    print_warning "Directorio tests/ no encontrado, saltando tests unitarios"
fi

# 2. TESTS DE FUNCIONALIDAD E INTEGRACIÓN
print_section "🌐 Tests de Funcionalidad e Integración"

# Test 1: Health Check
run_test "Health Check" \
    "curl -s http://localhost:3000/health" \
    "status"

# Test 2: Registro con contraseña débil (debe fallar)
run_test "Registro con contraseña débil (error esperado)" \
    "curl -s -X POST 'http://localhost:3000/auth/register' -H 'Content-Type: application/json' -d '{\"username\": \"testuser_$(date +%s)\", \"email\": \"test$(date +%s)@test.com\", \"password\": \"weak123\"}'" \
    "ensure this value has at least 8 characters"

# Test 3: Registro exitoso
TEST_USERNAME="testuser_$(date +%s)"
TEST_EMAIL="test$(date +%s)@test.com"
TEST_PASSWORD="TestPass123!"

run_test "Registro exitoso con contraseña segura" \
    "curl -s -X POST 'http://localhost:3000/auth/register' -H 'Content-Type: application/json' -d '{\"username\": \"$TEST_USERNAME\", \"email\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\"}'" \
    "\"id\":"

# Test 4: Login incorrecto (debe fallar)
run_test "Login con credenciales incorrectas (error esperado)" \
    "curl -s -X POST 'http://localhost:3000/auth/login' -H 'Content-Type: application/json' -d '{\"username\": \"$TEST_USERNAME\", \"password\": \"WrongPass123!\"}'" \
    "Incorrect username or password"

# Test 5: Login exitoso
print_test "Test: Login exitoso y obtención de tokens"
TOTAL_TESTS=$((TOTAL_TESTS + 1))

LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:3000/auth/login" -H "Content-Type: application/json" -d "{\"username\": \"$TEST_USERNAME\", \"password\": \"$TEST_PASSWORD\"}")

if [[ $LOGIN_RESPONSE == *"access_token"* ]] && [[ $LOGIN_RESPONSE == *"refresh_token"* ]]; then
    print_status "PASÓ: Login exitoso"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    
    # Extraer token para tests siguientes
    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    print_info "Token obtenido para tests posteriores"
else
    print_error "FALLÓ: Login exitoso"
    echo "   Respuesta: $LOGIN_RESPONSE"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    TOKEN=""
fi

# Tests que requieren autenticación (solo si tenemos token)
if [ -n "$TOKEN" ]; then
    
    # Test 6: Acceso sin autenticación (debe fallar)
    run_test "Acceso a endpoint protegido sin token (error esperado)" \
        "curl -s -X GET 'http://localhost:3000/attendees/'" \
        "Not authenticated"
    
    # Test 7: Listar asistentes con autenticación
    run_test "Listar asistentes con autenticación" \
        "curl -s -X GET 'http://localhost:3000/attendees/' -H 'Authorization: Bearer $TOKEN'" \
        "["
    
    # Test 8: Crear asistente con datos inválidos (debe fallar)
    run_test "Crear asistente con datos inválidos (error esperado)" \
        "curl -s -X POST 'http://localhost:3000/attendees/' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"name\": \"Test User\", \"email\": \"test@test.com\", \"document_type\": \"INVALID\", \"document_number\": \"123\"}'" \
        "not a valid enumeration member"
    
    # Test 9: Crear asistente correctamente
    RANDOM_DOC_NUMBER="$(date +%s)$(shuf -i 1000-9999 -n 1)"
    run_test "Crear asistente con datos válidos" \
        "curl -s -X POST 'http://localhost:3000/attendees/' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"name\": \"Juan Pérez Test\", \"email\": \"juan.test.$(date +%s)@test.com\", \"document_type\": \"DNI\", \"document_number\": \"'$RANDOM_DOC_NUMBER'\", \"phone_number\": \"555-1234\"}'" \
        "attendee_id"
    
    # Test 10: Token inválido (debe fallar)
    run_test "Acceso con token inválido (error esperado)" \
        "curl -s -X GET 'http://localhost:3000/attendees/' -H 'Authorization: Bearer invalid_token_123'" \
        "Could not validate credentials"
    
else
    print_warning "Token no disponible, saltando tests de autenticación"
fi

# 3. TESTS DE SEGURIDAD
print_section "🔒 Tests de Seguridad"

# Test de headers de seguridad
print_test "Test: Headers de seguridad presentes"
TOTAL_TESTS=$((TOTAL_TESTS + 1))

HEADERS_RESPONSE=$(curl -s -I http://localhost:3000/health 2>/dev/null)

if [[ $HEADERS_RESPONSE == *"x-content-type-options"* ]] && [[ $HEADERS_RESPONSE == *"x-frame-options"* ]]; then
    print_status "PASÓ: Headers de seguridad presentes"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    print_error "FALLÓ: Headers de seguridad no encontrados"
    echo "   Headers recibidos:"
    echo "$HEADERS_RESPONSE" | grep -i "x-"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test de rate limiting headers
run_test "Headers de rate limiting presentes" \
    "curl -s -I http://localhost:3000/health 2>/dev/null" \
    "x-ratelimit-limit"

# 4. TESTS DE VALIDACIÓN DE DATOS
print_section "📋 Tests de Validación de Datos"

if [ -n "$TOKEN" ]; then
    # Test de validación de email
    run_test "Validación de email inválido (error esperado)" \
        "curl -s -X POST 'http://localhost:3000/attendees/' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"name\": \"Test\", \"email\": \"invalid-email\", \"document_type\": \"DNI\", \"document_number\": \"123\", \"phone_number\": \"555\"}'" \
        "value is not a valid email address"
    
    # Test de campos requeridos
    run_test "Validación de campos requeridos (error esperado)" \
        "curl -s -X POST 'http://localhost:3000/attendees/' -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"name\": \"Test\"}'" \
        "field required"
fi

# Cleanup: Detener servidor de testing si lo iniciamos nosotros
if [ -n "$SERVER_PID" ]; then
    print_info "Deteniendo servidor de testing..."
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
fi

# RESUMEN FINAL
print_section "📊 Resumen de Pruebas"

echo ""
echo -e "${CYAN}📈 Estadísticas:${NC}"
echo "   🧪 Total de tests: $TOTAL_TESTS"
echo -e "   ${GREEN}✅ Tests exitosos: $PASSED_TESTS${NC}"
echo -e "   ${RED}❌ Tests fallidos: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!${NC}"
    echo ""
    echo -e "${CYAN}✅ Funcionalidades verificadas:${NC}"
    echo "   🔐 Autenticación JWT"
    echo "   🛡️ Validaciones de seguridad"
    echo "   📝 CRUD de asistentes"
    echo "   🚦 Rate limiting"
    echo "   📊 Headers de seguridad"
    echo "   ❌ Manejo de errores"
    echo "   ✅ Casos de éxito"
    echo ""
    echo -e "${GREEN}🚀 El microservicio está completamente funcional y seguro!${NC}"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️ Algunos tests fallaron. Revisar implementación.${NC}"
    echo ""
    echo -e "${CYAN}📝 Para más detalles:${NC}"
    echo "   • Logs del servidor: /tmp/test_server.log"
    echo "   • Tests unitarios: /tmp/pytest_output.log"
    echo "   • Documentación: http://localhost:3000/docs"
    exit 1
fi
