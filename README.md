# API de Precios de Combustibles

API para consultar precios de combustibles de Osinergmin.

## Despliegue en Render

1. Crea una cuenta en [Render](https://render.com) si aún no tienes una.

2. Conecta tu repositorio de GitHub con Render.

3. Crea un nuevo servicio web en Render:
   - Selecciona tu repositorio
   - Nombre: api-precios
   - Runtime: Python 3.9
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. La aplicación se desplegará automáticamente y estará disponible en la URL proporcionada por Render.

## Variables de Entorno

No se requieren variables de entorno adicionales para el funcionamiento básico de la API.

## Documentación de la API

Una vez desplegada, puedes acceder a la documentación de la API en:
- Swagger UI: `https://tu-app.onrender.com/docs`
- ReDoc: `https://tu-app.onrender.com/redoc`

## Desarrollo Local

1. Clona el repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Ejecuta la aplicación: `python run.py`

La API estará disponible en `http://localhost:8000`