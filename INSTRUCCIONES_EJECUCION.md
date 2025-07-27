# Instrucciones para ejecutar los proyectos

Este documento detalla cómo ejecutar simultáneamente el proyecto Django (admin_events) y la API FastAPI (admin_events_attendees) que interactúa con la base de datos de Django.

## Requisitos previos

- Python 3.x instalado
- Gestor de paquetes pip
- Postman (para probar la API)

## Configuración del proyecto Django

1. Crear y activar el entorno virtual para Django:

```bash
# En la raíz del proyecto admin_events
cd /Users/anderson/Miso/modernizacion/entrega_7/admin_events
python -m venv .venv_django
source .venv_django/bin/activate  # En macOS/Linux
# En Windows usar: .venv_django\Scripts\activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor Django:

```bash
cd admin_manage_events
python manage.py runserver
```

El servidor Django estará disponible en: http://localhost:8000

## Configuración de la API FastAPI

1. Crear y activar el entorno virtual para FastAPI:

```bash
# En la raíz del proyecto admin_events_attendees
cd /Users/anderson/Miso/modernizacion/entrega_7/admin_events_attendees
python -m venv .venv_api
source .venv_api/bin/activate  # En macOS/Linux
# En Windows usar: .venv_api\Scripts\activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor FastAPI:

```bash
python main.py
```

La API FastAPI estará disponible en: http://localhost:3000

## Documentación de la API

- Documentación interactiva Swagger UI: http://localhost:3000/docs
- Documentación alternativa ReDoc: http://localhost:3000/redoc

## Probando la API con Postman

1. Importar la colección de Postman actualizada:
   - Abrir Postman
   - Importar el archivo `admin_events_attendees/attendees_api_postman_collection.json`

2. La colección ya está configurada para usar el puerto 3000 donde se ejecuta FastAPI.

3. Ejecutar los endpoints para interactuar con la base de datos de Django.

## Notas importantes

- Asegúrate de que el servidor Django esté en ejecución antes de usar la API FastAPI, ya que esta última necesita acceder a la base de datos SQLite de Django.
- Los dos servidores deben ejecutarse en terminales separadas y con sus respectivos entornos virtuales activados.
- La API FastAPI está configurada para conectarse a la base de datos SQLite en la ruta: `/Users/anderson/Miso/modernizacion/entrega_7/admin_events/admin_manage_events/db.sqlite3`.

## Solución de problemas comunes

- **Error "ModuleNotFoundError"**: Asegúrate de tener activado el entorno virtual correcto y de haber instalado todas las dependencias.
- **Error al conectar a la base de datos**: Verifica que la ruta a la base de datos en la configuración de FastAPI sea correcta.
- **Conflicto de puertos**: Si alguno de los puertos ya está en uso, puedes cambiar el puerto agregando el número de puerto al comando de ejecución (por ejemplo, `python manage.py runserver 8001` para Django o modificando la configuración en `main.py` para FastAPI).
