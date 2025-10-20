#!/bin/bash

# Script para probar el microservicio desplegado en AWS Beanstalk
# Universidad de los Andes - MISW4304

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
SECRET_TOKEN="test_secret_token_123"

echo -e "${BLUE}🧪 Probando Microservicio Blacklist en Producción${NC}"
echo -e "${BLUE}===============================================${NC}"

# Verificar que se proporcione la URL
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Debes proporcionar la URL de la aplicación${NC}"
    echo -e "${YELLOW}💡 Uso: ./test_production.sh https://tu-app.elasticbeanstalk.com${NC}"
    exit 1
fi

BASE_URL="$1"
echo -e "${YELLOW}🔗 URL de la aplicación: $BASE_URL${NC}"
echo ""

# Función para hacer requests
make_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local headers="$4"
    
    if [ "$method" = "GET" ]; then
        curl -s -w "\n%{http_code}" -H "$headers" "$BASE_URL$endpoint"
    else
        curl -s -w "\n%{http_code}" -X "$method" -H "$headers" -d "$data" "$BASE_URL$endpoint"
    fi
}

# Test 1: Health Check
echo -e "${BLUE}🔍 Test 1: Health Check${NC}"
response=$(make_request "GET" "/blacklists/ping" "" "")
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Health check exitoso (HTTP $http_code)${NC}"
    echo -e "${GREEN}📝 Respuesta: $response_body${NC}"
else
    echo -e "${RED}❌ Health check falló (HTTP $http_code)${NC}"
    echo -e "${RED}📝 Respuesta: $response_body${NC}"
fi
echo ""

# Test 2: Agregar Email a Lista Negra
echo -e "${BLUE}📧 Test 2: Agregar Email a Lista Negra${NC}"
test_email="test_$(date +%s)@example.com"
test_uuid="550e8400-e29b-41d4-a716-446655440000"

headers="Authorization: Bearer $SECRET_TOKEN
Content-Type: application/json"

data="{
    \"email\": \"$test_email\",
    \"app_uuid\": \"$test_uuid\",
    \"blocked_reason\": \"Test desde script de producción\"
}"

response=$(make_request "POST" "/blacklists" "$data" "$headers")
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

if [ "$http_code" = "201" ]; then
    echo -e "${GREEN}✅ Email agregado exitosamente (HTTP $http_code)${NC}"
    echo -e "${GREEN}📝 Respuesta: $response_body${NC}"
    echo -e "${GREEN}📧 Email de prueba: $test_email${NC}"
else
    echo -e "${RED}❌ Error al agregar email (HTTP $http_code)${NC}"
    echo -e "${RED}📝 Respuesta: $response_body${NC}"
fi
echo ""

# Test 3: Verificar Email en Lista Negra
echo -e "${BLUE}🔍 Test 3: Verificar Email en Lista Negra${NC}"
headers="Authorization: Bearer $SECRET_TOKEN"

response=$(make_request "GET" "/blacklists/$test_email" "" "$headers")
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Verificación exitosa (HTTP $http_code)${NC}"
    echo -e "${GREEN}📝 Respuesta: $response_body${NC}"
else
    echo -e "${RED}❌ Error en verificación (HTTP $http_code)${NC}"
    echo -e "${RED}📝 Respuesta: $response_body${NC}"
fi
echo ""

# Test 4: Verificar Email No Existente
echo -e "${BLUE}🔍 Test 4: Verificar Email No Existente${NC}"
nonexistent_email="nonexistent_$(date +%s)@example.com"

response=$(make_request "GET" "/blacklists/$nonexistent_email" "" "$headers")
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Verificación de email no existente exitosa (HTTP $http_code)${NC}"
    echo -e "${GREEN}📝 Respuesta: $response_body${NC}"
else
    echo -e "${RED}❌ Error en verificación de email no existente (HTTP $http_code)${NC}"
    echo -e "${RED}📝 Respuesta: $response_body${NC}"
fi
echo ""

# Test 5: Token Inválido
echo -e "${BLUE}🔒 Test 5: Token Inválido${NC}"
invalid_headers="Authorization: Bearer invalid_token
Content-Type: application/json"

data="{
    \"email\": \"test_invalid@example.com\",
    \"app_uuid\": \"$test_uuid\",
    \"blocked_reason\": \"Test con token inválido\"
}"

response=$(make_request "POST" "/blacklists" "$data" "$invalid_headers")
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

if [ "$http_code" = "401" ]; then
    echo -e "${GREEN}✅ Autenticación funcionando correctamente (HTTP $http_code)${NC}"
    echo -e "${GREEN}📝 Respuesta: $response_body${NC}"
else
    echo -e "${RED}❌ Error en autenticación (HTTP $http_code)${NC}"
    echo -e "${RED}📝 Respuesta: $response_body${NC}"
fi
echo ""

# Resumen
echo -e "${BLUE}📊 Resumen de Pruebas${NC}"
echo -e "${BLUE}===================${NC}"
echo -e "${GREEN}✅ Tests completados${NC}"
echo -e "${YELLOW}🔗 URL de la aplicación: $BASE_URL${NC}"
echo -e "${YELLOW}📧 Email de prueba usado: $test_email${NC}"
echo -e "${YELLOW}🔑 Token usado: $SECRET_TOKEN${NC}"
echo ""
echo -e "${BLUE}💡 Próximos pasos:${NC}"
echo -e "1. Ejecutar tests Newman en producción"
echo -e "2. Configurar RDS PostgreSQL"
echo -e "3. Implementar estrategias de despliegue"
echo -e "4. Documentar con capturas de pantalla"
