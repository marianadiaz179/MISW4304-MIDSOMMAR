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

La documentación de postman la puedes encontrar [aqui](https://documenter.getpostman.com/view/25797145/2sB3QQKTZn)

### 1. Agregar un email a la lista negra global

**EP:** `POST /blacklists`

**Descripción:** Agrega un correo electrónico a la lista negra; solo los usuarios autenticados pueden hacerlo.

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
   
   3.1. Falta un parametro
   ```json
    {
        "msg": "Missing parameter {param}"
    }
    ```
   3.2. Los parametros no son strings
   ```json
    {
        "msg": "{param} must be a string."
    }
    ```
   3.3. El email no es valido
   ```json
    {
        "msg": "email is not a valid email"
    }
    ```
   3.4. app_uuid no es un UUID
    ```json
    {
        "msg": "app_uuid is not a valid UUID"
    }
    ```
   3.5. blocked_reason tiene mas de 255 caracteres
   ```json
    {
        "msg": "blocked_reason must have a maximum of 255 characters"
    }
    ```
