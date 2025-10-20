# 🚀 Estrategias de Despliegue - AWS Beanstalk

**Universidad de los Andes - MISW4304**  
*Documentación de 4 Estrategias de Despliegue*

## 📋 Resumen

Este documento detalla las 4 estrategias de despliegue requeridas para el proyecto, incluyendo configuración, ejecución y documentación de resultados.

## 🎯 Configuración Base

### Auto Scaling Group
- **Mínimo**: 3 instancias
- **Máximo**: 6 instancias
- **Tipo de instancia**: t3.micro (para pruebas)
- **Health check**: `/blacklists/ping`

### Configuración Inicial
1. Crear aplicación en AWS Beanstalk
2. Configurar Auto Scaling Group (3-6 instancias)
3. Configurar RDS PostgreSQL
4. Configurar variables de entorno
5. Desplegar versión inicial

## 🔄 Estrategia 1: All-at-Once

### Configuración
- **Deployment Policy**: All at once
- **Instancias**: 3-6 instancias
- **Tiempo de inactividad**: Alto
- **Riesgo**: Alto

### Pasos de Implementación
1. **Configurar en Beanstalk Console**
   - Ir a Configuration > Rolling updates and deployments
   - Deployment policy: `All at once`
   - Guardar configuración

2. **Ejecutar Despliegue**
   - Subir nueva versión del código
   - Iniciar despliegue
   - Monitorear proceso

3. **Documentar Resultados**
   - [ ] Tiempo total de despliegue: ___ minutos ___ segundos
   - [ ] Instancias utilizadas: ___
   - [ ] Despliegue en instancias: [ ] Iniciales [ ] Nuevas
   - [ ] Tiempo de inactividad: ___ minutos
   - [ ] Capturas de pantalla del proceso

### Hallazgos Esperados
- **Ventajas**: Despliegue rápido, todas las instancias actualizadas simultáneamente
- **Desventajas**: Alto tiempo de inactividad, riesgo de fallo total
- **Uso recomendado**: Entornos de desarrollo o aplicaciones que pueden tolerar inactividad

## 🔄 Estrategia 2: Rolling

### Configuración
- **Deployment Policy**: Rolling
- **Batch size**: 1
- **Instancias**: 3-6 instancias
- **Tiempo de inactividad**: Mínimo
- **Riesgo**: Medio

### Pasos de Implementación
1. **Configurar en Beanstalk Console**
   - Deployment policy: `Rolling`
   - Batch size: `1`
   - Guardar configuración

2. **Ejecutar Despliegue**
   - Subir nueva versión del código
   - Iniciar despliegue
   - Monitorear proceso

3. **Documentar Resultados**
   - [ ] Tiempo total de despliegue: ___ minutos ___ segundos
   - [ ] Instancias utilizadas: ___
   - [ ] Despliegue en instancias: [ ] Iniciales [ ] Nuevas
   - [ ] Tiempo de inactividad: ___ minutos
   - [ ] Capturas de pantalla del proceso

### Hallazgos Esperados
- **Ventajas**: Mínimo tiempo de inactividad, despliegue gradual
- **Desventajas**: Tiempo de despliegue más largo, complejidad en rollback
- **Uso recomendado**: Aplicaciones de producción que requieren alta disponibilidad

## 🔄 Estrategia 3: Rolling with Additional Batch

### Configuración
- **Deployment Policy**: Rolling with additional batch
- **Batch size**: 2
- **Instancias**: 3-6 instancias
- **Tiempo de inactividad**: Mínimo
- **Riesgo**: Medio-Bajo

### Pasos de Implementación
1. **Configurar en Beanstalk Console**
   - Deployment policy: `Rolling with additional batch`
   - Batch size: `2`
   - Guardar configuración

2. **Ejecutar Despliegue**
   - Subir nueva versión del código
   - Iniciar despliegue
   - Monitorear proceso

3. **Documentar Resultados**
   - [ ] Tiempo total de despliegue: ___ minutos ___ segundos
   - [ ] Instancias utilizadas: ___
   - [ ] Despliegue en instancias: [ ] Iniciales [ ] Nuevas
   - [ ] Tiempo de inactividad: ___ minutos
   - [ ] Capturas de pantalla del proceso

### Hallazgos Esperados
- **Ventajas**: Balance entre velocidad y disponibilidad, capacidad adicional durante despliegue
- **Desventajas**: Mayor costo temporal, complejidad en gestión de instancias
- **Uso recomendado**: Aplicaciones con alta carga que requieren capacidad adicional

## 🔄 Estrategia 4: Immutable

### Configuración
- **Deployment Policy**: Immutable
- **Instancias**: 3-6 instancias
- **Tiempo de inactividad**: Mínimo
- **Riesgo**: Muy Bajo

### Pasos de Implementación
1. **Configurar en Beanstalk Console**
   - Deployment policy: `Immutable`
   - Guardar configuración

2. **Ejecutar Despliegue**
   - Subir nueva versión del código
   - Iniciar despliegue
   - Monitorear proceso

3. **Documentar Resultados**
   - [ ] Tiempo total de despliegue: ___ minutos ___ segundos
   - [ ] Instancias utilizadas: ___
   - [ ] Despliegue en instancias: [ ] Iniciales [ ] Nuevas
   - [ ] Tiempo de inactividad: ___ minutos
   - [ ] Capturas de pantalla del proceso

### Hallazgos Esperados
- **Ventajas**: Máxima disponibilidad, rollback automático en caso de fallo
- **Desventajas**: Mayor tiempo de despliegue, mayor uso de recursos
- **Uso recomendado**: Aplicaciones críticas de producción

## 📊 Plantilla de Documentación

### Para Cada Estrategia

```markdown
## Estrategia X: [Nombre]

### Configuración Aplicada
- Deployment Policy: [Policy]
- Batch Size: [Size]
- Instancias: [Number]

### Resultados del Despliegue
- **Tiempo total**: [X] minutos [Y] segundos
- **Instancias utilizadas**: [Number]
- **Tipo de despliegue**: [Iniciales/Nuevas]
- **Tiempo de inactividad**: [X] minutos
- **Estado final**: [Exitoso/Fallido]

### Capturas de Pantalla
- [ ] Configuración inicial
- [ ] Proceso de despliegue
- [ ] Resultados finales
- [ ] Métricas de performance

### Hallazgos
[Descripción detallada de los hallazgos]

### Recomendaciones
[Recomendaciones basadas en los resultados]
```

## 🧪 Validación Post-Despliegue

### Para Cada Estrategia

1. **Health Check**
   ```bash
   curl https://[app-url].elasticbeanstalk.com/blacklists/ping
   ```

2. **Prueba de Endpoints**
   ```bash
   # Agregar email
   curl -X POST https://[app-url].elasticbeanstalk.com/blacklists \
     -H "Authorization: Bearer [token]" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","app_uuid":"[uuid]","blocked_reason":"Test"}'
   
   # Verificar email
   curl https://[app-url].elasticbeanstalk.com/blacklists/test@example.com \
     -H "Authorization: Bearer [token]"
   ```

3. **Pruebas con Newman**
   ```bash
   newman run Blacklist_Microservice_With_Tests.postman_collection.json \
     --global-var "base_url=https://[app-url].elasticbeanstalk.com" \
     --global-var "secret_token=[token]"
   ```

## 📈 Métricas a Documentar

### Tiempo de Despliegue
- Tiempo de inicio del despliegue
- Tiempo de finalización del despliegue
- Tiempo total calculado

### Disponibilidad
- Tiempo de inactividad total
- Porcentaje de disponibilidad durante despliegue
- Impacto en usuarios

### Recursos
- Número de instancias utilizadas
- Uso de CPU durante despliegue
- Uso de memoria durante despliegue
- Costo estimado del despliegue

## 🎯 Conclusiones Esperadas

### Comparación de Estrategias

| Estrategia | Tiempo | Inactividad | Riesgo | Costo | Recomendación |
|------------|--------|-------------|--------|-------|---------------|
| All-at-Once | Bajo | Alto | Alto | Bajo | Desarrollo |
| Rolling | Medio | Bajo | Medio | Medio | Producción |
| Rolling + Batch | Medio | Bajo | Medio | Alto | Alta Carga |
| Immutable | Alto | Mínimo | Bajo | Alto | Crítico |

### Recomendaciones Finales
- **Desarrollo**: All-at-Once
- **Staging**: Rolling
- **Producción**: Rolling o Immutable
- **Aplicaciones Críticas**: Immutable

---

**Universidad de los Andes - MISW4304**  
*Estrategias de Despliegue - Microservicio Blacklist*
