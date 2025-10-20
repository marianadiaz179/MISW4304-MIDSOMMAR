# 🔧 Variables de Entorno - AWS Beanstalk

**Universidad de los Andes - MISW4304**  
*Configuración de Variables de Entorno para el Microservicio Blacklist*

## 📋 Variables Requeridas

### Base de Datos
```
DB_USER=postgres
DB_PASSWORD=tu_password_seguro_aqui
DB_HOST=tu_rds_endpoint_aqui
DB_NAME=blacklist_db
```

### Autenticación
```
SECRET_TOKEN=tu_secret_token_jwt_aqui
```

### Flask
```
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🚀 Cómo Configurar en AWS Beanstalk

### Paso 1: Acceder a la Configuración
1. **Ir a tu aplicación en AWS Beanstalk**
2. **Seleccionar el entorno**
3. **En el menú izquierdo, hacer clic en "Configuration"**
4. **Hacer clic en "Software"**

### Paso 2: Agregar Variables de Entorno
1. **Hacer clic en "Edit"**
2. **En la sección "Environment properties"**
3. **Agregar cada variable una por una:**

#### Variable 1: DB_USER
- **Name**: `DB_USER`
- **Value**: `postgres`

#### Variable 2: DB_PASSWORD
- **Name**: `DB_PASSWORD`
- **Value**: `[tu_password_seguro]`

#### Variable 3: DB_HOST
- **Name**: `DB_HOST`
- **Value**: `[endpoint_de_tu_rds]`

#### Variable 4: DB_NAME
- **Name**: `DB_NAME`
- **Value**: `blacklist_db`

#### Variable 5: SECRET_TOKEN
- **Name**: `SECRET_TOKEN`
- **Value**: `[tu_secret_token]`

#### Variable 6: FLASK_ENV
- **Name**: `FLASK_ENV`
- **Value**: `production`

#### Variable 7: FLASK_DEBUG
- **Name**: `FLASK_DEBUG`
- **Value**: `False`

### Paso 3: Aplicar Cambios
1. **Hacer clic en "Apply"**
2. **Esperar a que se reinicie la aplicación**
3. **Verificar que el estado sea "OK"**

## 🔐 Valores de Ejemplo

### Para Pruebas (Desarrollo)
```
DB_USER=postgres
DB_PASSWORD=password123
DB_HOST=localhost
DB_NAME=blacklist_db
SECRET_TOKEN=test_secret_token_123
FLASK_ENV=development
FLASK_DEBUG=True
```

### Para Producción
```
DB_USER=postgres
DB_PASSWORD=SuperSecurePassword2024!
DB_HOST=blacklist-db.xyz123.us-east-1.rds.amazonaws.com
DB_NAME=blacklist_db
SECRET_TOKEN=prod_secret_token_xyz789
FLASK_ENV=production
FLASK_DEBUG=False
```

## ⚠️ Consideraciones de Seguridad

### Password de Base de Datos
- **Mínimo 8 caracteres**
- **Incluir mayúsculas, minúsculas, números y símbolos**
- **No usar contraseñas comunes**
- **Ejemplo**: `MySecureDB2024!`

### Secret Token JWT
- **Mínimo 32 caracteres**
- **Usar caracteres aleatorios**
- **No compartir en código**
- **Ejemplo**: `jwt_secret_xyz789_abc123_def456`

## 🧪 Verificar Configuración

### Test de Variables
Una vez configuradas, puedes verificar que las variables estén funcionando:

```bash
# Health check
curl https://tu-app.elasticbeanstalk.com/blacklists/ping

# Test con token
curl -X POST https://tu-app.elasticbeanstalk.com/blacklists \
  -H "Authorization: Bearer [tu_secret_token]" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "Test variables"
  }'
```

## 📝 Notas Importantes

1. **Las variables son sensibles**: No las compartas públicamente
2. **Reinicio automático**: Beanstalk reiniciará la aplicación al cambiar variables
3. **Verificación**: Siempre verifica que la aplicación funcione después de cambios
4. **Backup**: Mantén un registro de las variables configuradas

## 🔄 Actualizar Variables

Para actualizar una variable:
1. **Ir a Configuration > Software**
2. **Hacer clic en "Edit"**
3. **Modificar el valor de la variable**
4. **Hacer clic en "Apply"**
5. **Esperar el reinicio**

---

**Universidad de los Andes - MISW4304**  
*Variables de Entorno - Microservicio Blacklist*
