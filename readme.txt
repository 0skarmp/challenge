# Contacts API

## Descripción
API REST para gestión de contactos.

## Niveles implementados
- Nivel 1: CRUD
- Nivel 2: Validaciones + manejo de errores
- Nivel 3: Swagger
- Nivel 4: Docker
- Bonus: Paginación y filtro por email

## Ejecutar local
pip install -r requirements.txt
python -m app.main

## Docker
docker build -t contacts-api .
docker run -p 5000:5000 contacts-api

## Environment variables (opcional)

Puedes crear un archivo `.env` en la raíz del proyecto para sobreescribir valores de configuración como la URL de la base de datos o el entorno de Flask. La aplicación utiliza `python-dotenv` y carga este archivo automáticamente.

Ejemplo de `.env`:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///contacts.db
```

## Swagger
http://localhost:5000/apidocs