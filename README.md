# MISW4304-MIDSOMMAR

## Descripción

Esta sección describe los servicios desarrollados en Python 3.12 utilizando Flask como framework y PostgreSQL como base de datos.

## Configuración del entorno

En la raíz del proyecto, debe existir un archivo .env con la siguiente configuración:

```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_TOKEN=
```

1. Crear un entorno virtual:

```
python -m venv venv
```

2. Activar el entorno virtual:

```
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

3. Instalar dependencias:

```
cd api
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

Desde la raiz del repositorio

```
python -m api.src.app
```

## Descripción de los endpoints

### 1. Agregar un email a la lista negra global

**EP:** `POST /blacklist`

**Descripción:** Crea una nueva cuenta en la blacklist. Solo los usuarios autenticados pueden crear una blacklist.

**Datos de entrada (JSON):**

```json
{
  "email": "correo eletrónico de la cuenta",
  "app_uuid": "uuid de la apicación",
  "blocked_reason": "razón por la que fue agregado a la blacklist (opcional)"
}
```

**Datos de salida (JSON):**

1. Cuando una solicitud POST se procesa correctamente, el servidor devuelve un código de estado 201 y un mensaje de:

```json
{
  "msg": "Email added to the blacklist"
}
```

2. Cuando el email ya esta en la blacklist, el servidor devuelve un código de estado 409 y un mensaje de:

```json
{
  "msg": "Email is already in the blacklist"
}
```

3. Cuando la validacion del payload falla, el servidor devuelve un código de estado 400 y un mensaje de:

```json
// Falta un parametro
{
    "msg": "Missing parameter {param}"
}
// Los parametros no son strings
{
    "msg": "{param} must be a string."
}
// El email no es valido
{
    "msg": "email is not a valid email"
}
// app_uuid no es un UUID
{
    "msg": "app_uuid is not a valid UUID"
}
// blocked_reason tiene mas de 255 caracteres
{
    "msg": "blocked_reason must have a maximum of 255 characters"
}
```
