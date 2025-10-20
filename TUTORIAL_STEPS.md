# 📋 Pasos del Tutorial AWS Beanstalk - Microservicio Blacklist

**Universidad de los Andes - MISW4304**  
*Siguiendo el Tutorial Oficial de AWS Beanstalk*

## 🎯 Objetivo
Desplegar el microservicio Blacklist en AWS Elastic Beanstalk siguiendo el tutorial oficial paso a paso.

## 📦 Archivos Preparados
- ✅ `blacklist-microservice-deployment.zip` - Paquete listo para subir
- ✅ `application.py` - Punto de entrada (equivalente al del tutorial)
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `.ebextensions/` - Configuraciones de Beanstalk

## 🚀 Actividad 1: Creación de Rol del Perfil de Instancia EC2

### Paso 1: Acceder a IAM
1. **Iniciar sesión en AWS Console**
2. **Buscar y seleccionar IAM**
3. **En el panel izquierdo, seleccionar "Roles"**
4. **Hacer clic en "Crear rol"**

### Paso 2: Configurar el Rol
1. **Seleccionar "Servicio de AWS"**
2. **Caso de uso: seleccionar "EC2"**
3. **Hacer clic en "Siguiente"**

### Paso 3: Asignar Políticas
Seleccionar las siguientes políticas:
- ✅ `AWSElasticBeanstalkWebTier`
- ✅ `AWSElasticBeanstalkWorkerTier`
- ✅ `AWSElasticBeanstalkMulticontainerDocker`

**Hacer clic en "Siguiente"**

### Paso 4: Nombrar el Rol
- **Nombre del rol**: `Instance_Profile_EC2_Blacklist`
- **Descripción**: `Rol para perfil de instancia EC2 - Microservicio Blacklist`
- **Hacer clic en "Crear rol"**

## 🚀 Actividad 2: Despliegue de Aplicación en AWS Elastic Beanstalk

### Paso 1: Acceder a Elastic Beanstalk
1. **En el menú Servicios, seleccionar "Elastic Beanstalk"**
2. **Categoría: Informática**

### Paso 2: Crear Aplicación
1. **Hacer clic en "Create Application"**
2. **Nivel de entorno: "Entorno de servidor web"**
3. **Nombre de la aplicación**: `blacklist-microservice`

### Paso 3: Configurar Entorno
**Dejar valores por defecto en la información del entorno**

### Paso 4: Seleccionar Plataforma
- **Lenguaje de programación**: `Python`
- **Versión**: `Python 3.9` (o la más reciente disponible)
- **Configuración similar a la del tutorial**

### Paso 5: Código Fuente
- **Seleccionar**: "Aplicación de muestra"
- **Valores preestablecidos**: "Instancia única (compatible con la capa gratuita)"
- **Hacer clic en "Siguiente"**

### Paso 6: Configurar Acceso al Servicio
1. **Seleccionar "Crear rol"**
2. **Servicio**: "Elastic Beanstalk"
3. **Caso de uso**: "Elastic Beanstalk – Environment"
4. **Hacer clic en "Siguiente"**
5. **Dejar permisos por defecto**
6. **Nombre de rol por defecto**
7. **Hacer clic en "Crear rol"**

### Paso 7: Perfil de Instancia EC2
- **Seleccionar el rol creado en Actividad 1**: `Instance_Profile_EC2_Blacklist`
- **Hacer clic en "Siguiente"**

### Paso 8: Configuraciones Adicionales
- **Paso 3 (Red)**: Dejar por defecto
- **Paso 4 (Tamaño de instancias)**: 
  - Seleccionar "General Purpose 3 (SSD)"
  - **Deshabilitar IMDSv1** (importante desde Oct 2024)
- **Paso 5 (Monitoreo)**: Dejar por defecto

### Paso 9: Revisión y Creación
1. **Revisar configuración en Paso 6**
2. **Hacer clic en "Crear"**
3. **Esperar 5-15 minutos** para el aprovisionamiento

## 🚀 Actividad 3: Despliegue de Aplicación Flask

### Paso 1: Preparar Paquete
- ✅ **Archivo listo**: `blacklist-microservice-deployment.zip`
- ✅ **Estructura verificada**:
  - `application.py` (punto de entrada)
  - `requirements.txt` (dependencias)
  - `.ebextensions/` (configuraciones)
  - `src/` (código fuente)

### Paso 2: Cargar Aplicación
1. **Desde la vista de Entorno, hacer clic en "Cargar"**
2. **Etiqueta de versión**: `Version_1_Blacklist_API`
3. **Hacer clic en "Elegir archivo"**
4. **Seleccionar**: `blacklist-microservice-deployment.zip`
5. **Hacer clic en "Cargar"**

### Paso 3: Desplegar Aplicación
1. **Seleccionar la versión**: `Version_1_Blacklist_API`
2. **Menú "Acciones" → "Implementar"**
3. **Seleccionar el entorno**
4. **Hacer clic en "Implementar"**

### Paso 4: Verificar Despliegue
1. **Esperar que el estado sea "OK"**
2. **Acceder a la URL del dominio**
3. **Probar health check**: `GET /blacklists/ping`

## 🧪 Pruebas de la Aplicación

### Health Check
```bash
GET http://[ENV_NAME].us-east-1.elasticbeanstalk.com/blacklists/ping
```

### Agregar Email a Lista Negra
```bash
POST http://[ENV_NAME].us-east-1.elasticbeanstalk.com/blacklists
Authorization: Bearer [SECRET_TOKEN]
Content-Type: application/json

{
  "email": "test@example.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Test deployment"
}
```

### Verificar Email en Lista Negra
```bash
GET http://[ENV_NAME].us-east-1.elasticbeanstalk.com/blacklists/test@example.com
Authorization: Bearer [SECRET_TOKEN]
```

## 🔧 Configuraciones Adicionales

### Variables de Entorno
En **Configuration > Software**, agregar:
```
DB_USER=postgres
DB_PASSWORD=[tu_password]
DB_HOST=[rds_endpoint]
DB_NAME=blacklist_db
SECRET_TOKEN=[tu_secret_token]
FLASK_ENV=production
FLASK_DEBUG=False
```

### Health Check
En **Configuration > Load Balancer**:
- **Health check path**: `/blacklists/ping`
- **Health check interval**: 30 seconds
- **Healthy threshold**: 3
- **Unhealthy threshold**: 5

## 📊 Exploración del Entorno

Explorar las siguientes secciones:
- ✅ **Configuración**: Ver configuraciones del entorno
- ✅ **Registros**: Ver logs de la aplicación
- ✅ **Estado**: Estado actual del entorno
- ✅ **Monitorización**: Métricas de performance
- ✅ **Alarmas**: Configurar alertas
- ✅ **Actualizaciones administradas**: Gestión de actualizaciones
- ✅ **Eventos**: Historial de eventos

## 🧹 Limpieza (Al Final)

### Eliminar Aplicación
1. **Ir al listado de aplicaciones**
2. **Seleccionar la aplicación a eliminar**
3. **Menú "Acciones" → "Eliminar aplicación"**
4. **Confirmar eliminación**
5. **Esperar 2-10 minutos** para la terminación

## 📋 Checklist de Seguimiento

### Actividad 1 - Rol IAM
- [ ] Rol `Instance_Profile_EC2_Blacklist` creado
- [ ] Políticas asignadas correctamente
- [ ] Rol aparece en listado

### Actividad 2 - Aplicación Beanstalk
- [ ] Aplicación `blacklist-microservice` creada
- [ ] Entorno aprovisionado correctamente
- [ ] URL de acceso disponible
- [ ] Aplicación de muestra funcionando

### Actividad 3 - Despliegue Flask
- [ ] Paquete `blacklist-microservice-deployment.zip` cargado
- [ ] Versión `Version_1_Blacklist_API` desplegada
- [ ] Health check `/blacklists/ping` funcionando
- [ ] Endpoints de API respondiendo
- [ ] Variables de entorno configuradas

### Pruebas
- [ ] Health check exitoso
- [ ] POST /blacklists funcionando
- [ ] GET /blacklists/<email> funcionando
- [ ] Autenticación JWT funcionando
- [ ] Tests Newman ejecutándose en producción

## 🎯 Próximos Pasos

Después de completar el despliegue básico:
1. **Configurar RDS PostgreSQL**
2. **Implementar 4 estrategias de despliegue**
3. **Documentar con capturas de pantalla**
4. **Crear video de sustentación**

---

**Universidad de los Andes - MISW4304**  
*Pasos del Tutorial AWS Beanstalk - Microservicio Blacklist*
