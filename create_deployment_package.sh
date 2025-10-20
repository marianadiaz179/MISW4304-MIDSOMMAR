#!/bin/bash

# Script para crear el paquete de despliegue para AWS Beanstalk
# Universidad de los Andes - MISW4304

set -e

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Creando paquete de despliegue para AWS Beanstalk${NC}"
echo -e "${BLUE}================================================${NC}"

# Configuración
PACKAGE_NAME="blacklist-microservice-deployment.zip"
TEMP_DIR="deployment_temp"
API_DIR="api"

# Limpiar directorio temporal si existe
if [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}🧹 Limpiando directorio temporal...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Crear directorio temporal
echo -e "${YELLOW}📁 Creando directorio temporal...${NC}"
mkdir -p "$TEMP_DIR"

# Copiar archivos de la API
echo -e "${YELLOW}📦 Copiando archivos de la aplicación...${NC}"
cp -r "$API_DIR"/* "$TEMP_DIR/"

# Verificar que los archivos necesarios existen
echo -e "${YELLOW}🔍 Verificando archivos necesarios...${NC}"

required_files=(
    "application.py"
    "requirements.txt"
    "src/app.py"
    "src/config/config.py"
    "src/models/models.py"
    "src/routes/blacklist_router.py"
    "src/services/auth_service.py"
    "src/services/blacklist_service.py"
    ".ebextensions/01_packages.config"
    ".ebextensions/02_python.config"
    ".ebextensions/03_database.config"
    ".ebextensions/04_health.config"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$TEMP_DIR/$file" ]; then
        echo -e "${RED}❌ Archivo faltante: $file${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ $file${NC}"
    fi
done

# Crear el archivo ZIP
echo -e "${YELLOW}📦 Creando archivo ZIP...${NC}"
cd "$TEMP_DIR"
zip -r "../$PACKAGE_NAME" . -x "*.pyc" "__pycache__/*" "*.log" ".DS_Store"
cd ..

# Limpiar directorio temporal
echo -e "${YELLOW}🧹 Limpiando directorio temporal...${NC}"
rm -rf "$TEMP_DIR"

# Verificar el paquete creado
if [ -f "$PACKAGE_NAME" ]; then
    PACKAGE_SIZE=$(du -h "$PACKAGE_NAME" | cut -f1)
    echo -e "${GREEN}✅ Paquete creado exitosamente: $PACKAGE_NAME${NC}"
    echo -e "${GREEN}📊 Tamaño: $PACKAGE_SIZE${NC}"
    echo ""
    echo -e "${BLUE}📋 Próximos pasos:${NC}"
    echo -e "1. Ve a AWS Beanstalk Console"
    echo -e "2. Crea una nueva aplicación"
    echo -e "3. Sube el archivo: ${YELLOW}$PACKAGE_NAME${NC}"
    echo -e "4. Configura las variables de entorno"
    echo -e "5. Configura RDS para la base de datos"
    echo ""
    echo -e "${GREEN}🎉 ¡Paquete listo para despliegue!${NC}"
else
    echo -e "${RED}❌ Error al crear el paquete${NC}"
    exit 1
fi
