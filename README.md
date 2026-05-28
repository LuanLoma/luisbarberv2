# Plantilla Backend Flask + MariaDB

Esta plantilla acompaña al frontend Vue del proyecto base. Está diseñada para adaptarse a cualquier giro de negocio: barbería, taller mecánico, tienda, servicios, citas, inventario, etc.

## 1. Crear entorno virtual

```bash
    python -m venv venv
    venv\Scripts\activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Configurar variables de entorno

Copia `.env.example` como `.env` y ajusta tus datos:

```bash
copy .env.example .env
```

## 4. Crear base de datos

Ejecuta `schema.sql` en MariaDB.

## 5. Crear usuario de prueba

```bash
python create_user.py
```

Usuario creado:

- correo: `admin@luisbarber.com`
- contraseña: `12345`

## 6. Ejecutar servidor

```bash
python app.py
```

## Endpoints principales

- `GET /registros`
- `GET /registros/<id>`
- `POST /registros`
- `PUT /registros/<id>`
- `DELETE /registros/<id>`
- `POST /login`
- `GET /sesion`
- `POST /logout`
- `POST /contacto`

## Archivos principales

- `app.py`: rutas/endpoints.
- `db.py`: conexión a MariaDB.
- `validators.py`: validaciones mínimas.
- `security.py`: hash y verificación de contraseñas.
- `email_service.py`: envío de correo.
- `models.py`: clase base para registros.
