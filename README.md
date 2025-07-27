# admin_events_upgrade

## Descripción del Proyecto

Este proyecto demuestra una estrategia de modernización de software para la aplicación `admin_events`, implementando un enfoque de migración gradual hacia una arquitectura de microservicios. La modernización se centra en la extracción del módulo `attendees` del monolito Django original hacia un microservicio independiente desarrollado con FastAPI.

## Arquitectura de la Solución

### Componentes Principales

1. **Aplicación Monolítica Original (Django)**
   - **Ubicación**: `/admin_events/admin_manage_events/`
   - **Tecnología**: Django 4.2
   - **Función**: Sistema completo de gestión de eventos que incluye módulos para usuarios, eventos, asistentes, compras, tickets, gastos e ingresos.
   - **Base de datos**: SQLite ubicada en `/admin_events/admin_manage_events/db.sqlite3`

2. **Microservicio de Asistentes (FastAPI)**
   - **Ubicación**: `/admin_events_attendees/`
   - **Tecnología**: FastAPI + SQLAlchemy
   - **Función**: API REST que proporciona funcionalidades CRUD para gestionar asistentes, compras y tickets.
   - **Conexión**: Se conecta a la misma base de datos SQLite de Django utilizando SQLAlchemy con automap_base() para reflejar el esquema existente.

### Diagrama de Arquitectura

```
┌───────────────────────────┐      ┌────────────────────────────┐
│                           │      │                            │
│  Django Monolith          │      │  FastAPI Microservice      │
│  (admin_events)           │      │  (admin_events_attendees)  │
│                           │      │                            │
│  - Accounts               │      │  - Attendees API           │
│  - Events                 │      │  - Purchases API           │
│  - Expenses               │      │  - Tickets API             │
│  - Revenues               │      │                            │
│  - (legacy) Attendees     │◄─────┤  Reflects DB Schema        │
│                           │      │                            │
└───────────┬───────────────┘      └─────────────┬──────────────┘
            │                                    │
            │                                    │
            ▼                                    ▼
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│                     Shared SQLite Database                    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

# 🚀 Inicio Rápido

### Para Nuevos Usuarios (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd admin_events_upgrade/admin_events_attendees

# 2. Configuración automática completa
./setup.sh

# 3. Crear usuario administrador
./create_admin.sh

# 4. Ejecutar tests de seguridad
./run_tests.sh

# 5. Iniciar servidor
./start.sh
```

## Enfoque de Modernización

La estrategia de modernización implementada sigue un patrón "Strangler Fig" donde:

1. **Extracción de Funcionalidad**: El módulo de asistentes se ha extraído como un microservicio independiente.
2. **Coexistencia**: Ambos sistemas operan simultáneamente, compartiendo la misma base de datos.
3. **Compatibilidad**: El microservicio FastAPI respeta el esquema de datos y las restricciones definidas en Django.
4. **Mejoras Tecnológicas**: El nuevo microservicio aprovecha las ventajas de FastAPI como:
   - Mayor rendimiento (procesamiento asíncrono)
   - Validación automática con Pydantic
   - Documentación interactiva de la API (Swagger/OpenAPI)
   - Tipado estático para mayor robustez

## Ventajas de la Arquitectura

- **Modernización Incremental**: Permite actualizar el sistema por módulos sin interrumpir toda la aplicación.
- **Reducción de Riesgos**: Minimiza los riesgos al mantener el sistema original funcionando mientras se realizan migraciones graduales.
- **Especialización Tecnológica**: Utiliza la tecnología más adecuada para cada componente del sistema.
- **Flexibilidad de Despliegue**: Permite escalar independientemente el microservicio de asistentes según la demanda.
- **Mantenimiento Simplificado**: Facilita el mantenimiento al tener componentes más pequeños y especializados.

## Integración de Datos

El microservicio utiliza SQLAlchemy para conectarse a la base de datos SQLite de Django.
Se utiliza automap_base() para reflejar automáticamente el esquema de la base de datos existente.
Las entidades principales gestionadas son:
- **attendees_attendee**: Información de los asistentes
- **attendees_purchase**: Registro de compras
- **attendees_ticket**: Tickets asignados a asistentes

## Próximos Pasos en la Modernización

- Migración gradual de otros módulos a microservicios según sea necesario.
- Implementación de un API Gateway para enrutar peticiones a los distintos microservicios.
- Consideración de un servicio de descubrimiento para registro y localización de microservicios.
- Evaluación de la migración de SQLite a una base de datos más robusta para entornos de producción.


