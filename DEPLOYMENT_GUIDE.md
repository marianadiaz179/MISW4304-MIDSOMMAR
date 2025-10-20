# 🚀 Guía de Despliegue Manual - AWS Beanstalk

**Universidad de los Andes - MISW4304**  
*Despliegue Manual de Microservicio Blacklist*

## 📋 Resumen del Proyecto

Este documento describe el proceso de despliegue manual del microservicio de gestión de listas negras de emails en AWS Beanstalk, cumpliendo con los requisitos del proyecto de Universidad de los Andes MISW4304.

## 🎯 Objetivos del Despliegue

- Desplegar el microservicio en AWS Beanstalk
- Configurar RDS PostgreSQL para la base de datos
- Implementar 4 estrategias de despliegue diferentes
- Documentar el proceso completo con capturas de pantalla

## 📦 Preparación del Paquete de Despliegue

### 1. Crear el Paquete de Despliegue

```bash
# Ejecutar el script de creación de paquete
./create_deployment_package.sh
```

Este script creará un archivo `blacklist-microservice-deployment.zip` listo para subir a AWS Beanstalk.

### 2. Verificar Contenido del Paquete

El paquete incluye:
- ✅ `application.py` - Punto de entrada para Beanstalk
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `src/` - Código fuente de la aplicación
- ✅ `.ebextensions/` - Configuraciones de Beanstalk
- ✅ `Dockerfile` - Para despliegue con contenedores

## 🏗️ Configuración de AWS Beanstalk

### Paso 1: Crear Aplicación en Beanstalk

1. **Acceder a AWS Console**
   - Ir a AWS Elastic Beanstalk
   - Seleccionar región (recomendado: us-east-1)

2. **Crear Nueva Aplicación**
   - Nombre: `blacklist-microservice`
   - Descripción: `Microservicio de gestión de listas negras - MISW4304`

3. **Crear Entorno**
   - Plataforma: `Python 3.9`
   - Versión de plataforma: `Python 3.9 running on 64bit Amazon Linux 2`
   - Código de aplicación: `Subir archivo`

### Paso 2: Configurar Variables de Entorno

En la consola de Beanstalk, ir a **Configuration > Software** y agregar:

```
DB_USER = postgres
DB_PASSWORD = [tu_password_seguro]
DB_HOST = [endpoint_de_rds]
DB_NAME = blacklist_db
SECRET_TOKEN = [token_secreto_para_jwt]
FLASK_ENV = production
FLASK_DEBUG = False
```

### Paso 3: Configurar Health Check

En **Configuration > Load Balancer**:
- Health check path: `/blacklists/ping`
- Health check interval: 30 seconds
- Healthy threshold: 3
- Unhealthy threshold: 5

## 🗄️ Configuración de RDS PostgreSQL

### Paso 1: Crear Instancia RDS

1. **Acceder a RDS Console**
   - Ir a Amazon RDS
   - Crear base de datos

2. **Configuración de la Base de Datos**
   - Engine: PostgreSQL
   - Version: PostgreSQL 13.7
   - Template: Free tier (para pruebas)
   - DB instance identifier: `blacklist-db`
   - Master username: `postgres`
   - Master password: `[password_seguro]`
   - Database name: `blacklist_db`

3. **Configuración de Red**
   - VPC: Default VPC
   - Subnet group: Default
   - Public access: Yes (para pruebas)
   - Security group: Crear nuevo

### Paso 2: Configurar Security Group

1. **Crear Security Group**
   - Nombre: `blacklist-db-sg`
   - Descripción: `Security group para base de datos blacklist`

2. **Reglas de Entrada**
   - Type: PostgreSQL
   - Port: 5432
   - Source: Security group de Beanstalk

## 🚀 Estrategias de Despliegue

### Estrategia 1: All-at-Once

**Configuración:**
- Deployment policy: All at once
- Instancias: 3-6 instancias
- Tiempo de inactividad: Alto

**Pasos:**
1. Ir a **Configuration > Rolling updates and deployments**
2. Deployment policy: `All at once`
3. Desplegar nueva versión
4. Documentar tiempo de despliegue

### Estrategia 2: Rolling

**Configuración:**
- Deployment policy: Rolling
- Batch size: 1
- Instancias: 3-6 instancias

**Pasos:**
1. Deployment policy: `Rolling`
2. Batch size: `1`
3. Desplegar nueva versión
4. Documentar tiempo y comportamiento

### Estrategia 3: Rolling with Additional Batch

**Configuración:**
- Deployment policy: Rolling with additional batch
- Batch size: 2
- Instancias: 3-6 instancias

**Pasos:**
1. Deployment policy: `Rolling with additional batch`
2. Batch size: `2`
3. Desplegar nueva versión
4. Documentar tiempo y comportamiento

### Estrategia 4: Immutable

**Configuración:**
- Deployment policy: Immutable
- Instancias: 3-6 instancias
- Tiempo de inactividad: Mínimo

**Pasos:**
1. Deployment policy: `Immutable`
2. Desplegar nueva versión
3. Documentar tiempo y comportamiento

## 📊 Documentación Requerida

Para cada estrategia de despliegue, documentar:

### 1. Capturas de Pantalla
- [ ] Configuración de RDS
- [ ] Configuración del proyecto en AWS Beanstalk
- [ ] Configuración de health checks
- [ ] Proceso de despliegue en consola AWS
- [ ] Resultados del despliegue

### 2. Métricas por Estrategia
- [ ] Cantidad de instancias utilizadas
- [ ] Tiempo total de despliegue (minutos y segundos)
- [ ] Si el despliegue se realizó sobre instancias iniciales o nuevas
- [ ] Hallazgos encontrados de cada estrategia

### 3. Validación del Despliegue
- [ ] Health check funcionando
- [ ] Endpoints respondiendo correctamente
- [ ] Base de datos conectada
- [ ] Autenticación funcionando

## 🧪 Pruebas Post-Despliegue

### 1. Health Check
```bash
curl https://[tu-app].elasticbeanstalk.com/blacklists/ping
```

### 2. Prueba de Endpoints
```bash
# Agregar email a lista negra
curl -X POST https://[tu-app].elasticbeanstalk.com/blacklists \
  -H "Authorization: Bearer [tu_secret_token]" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "Test deployment"
  }'

# Verificar email en lista negra
curl https://[tu-app].elasticbeanstalk.com/blacklists/test@example.com \
  -H "Authorization: Bearer [tu_secret_token]"
```

### 3. Pruebas con Newman
```bash
# Actualizar URL en collection
# Ejecutar tests
newman run Blacklist_Microservice_With_Tests.postman_collection.json \
  --global-var "base_url=https://[tu-app].elasticbeanstalk.com" \
  --global-var "secret_token=[tu_secret_token]"
```

## 📝 Checklist de Despliegue

### Pre-Despliegue
- [ ] Paquete de despliegue creado
- [ ] Variables de entorno definidas
- [ ] RDS configurado
- [ ] Security groups configurados

### Despliegue
- [ ] Aplicación creada en Beanstalk
- [ ] Entorno configurado
- [ ] Variables de entorno configuradas
- [ ] Health checks configurados

### Post-Despliegue
- [ ] Health check funcionando
- [ ] Endpoints probados
- [ ] Base de datos conectada
- [ ] Newman tests ejecutados
- [ ] Documentación completada

## 🔧 Troubleshooting

### Problemas Comunes

1. **Error de Conexión a Base de Datos**
   - Verificar security groups
   - Verificar variables de entorno
   - Verificar endpoint de RDS

2. **Health Check Fallando**
   - Verificar ruta de health check
   - Verificar que la aplicación esté corriendo
   - Verificar logs de Beanstalk

3. **Error 500 en Endpoints**
   - Verificar logs de aplicación
   - Verificar configuración de Python
   - Verificar dependencias

### Logs de Beanstalk
- **Application logs**: `/var/log/eb-docker/containers/eb-current-app/`
- **Web server logs**: `/var/log/nginx/`
- **Health check logs**: `/var/log/eb-healthd/`

## 📚 Recursos Adicionales

- [AWS Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.0.x/deploying/)

---

**Universidad de los Andes - MISW4304**  
*Guía de Despliegue Manual - Microservicio Blacklist*
