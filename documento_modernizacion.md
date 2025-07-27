## Contexto y Análisis de la Aplicación Legado (Administrador de Eventos)

### Problemática que motiva la modernización

A partir del análisis del sistema legado [Administrador de Eventos](https://github.com/a-rodriguez-c/admin_events)), se identificaron las siguientes limitaciones críticas:
   
1. **Versión Obsoleta de Framework**
    - Uso de Django 4.2 (abril 2023) con parches de seguridad faltantes.
    - Django 5.2.3 LTS disponible desde abril 2025.
        
2. **Ausencia Total de Pruebas Automatizadas**
    - 0% de cobertura de tests (todos los archivos `tests.py` vacíos).
    - Refactor inseguro, alta probabilidad de introducir bugs.
        
3. **Fuerte Acoplamiento Backend**
    - Dependencia del Django Admin, sin separación clara de capas.
    - Lógica de negocio embebida en vistas y modelos, dificultando la modularización.
        
4. **Problemas Críticos de Rendimiento**
    
    - Consultas N+1 y sin paginación (EventAdmin carga todos los registros).
    - Alto consumo de memoria en listados masivos.
        
5. **Base de Datos No Escalable**
    - Uso de SQLite en producción, sin concurrencia ni replicación.
    - Riesgo de corrupción de datos y falta de backups automáticos.

---

### Motivador del negocio

- Mitigar riesgos de seguridad y garantizar cumplimiento normativo.
- Asegurar disponibilidad y escalabilidad durante picos de inscripción.
- Incrementar velocidad de despliegue y reducir costes operativos.
- Facilitar la evolución independiente de componentes mediante desacoplamiento para adaptarse ágilmente a cambios en requisitos de negocio.
    

---

### Respuestas a las preguntas de comprensión

- Según cartografía de procesos, los cuellos de botella clave están en la cola de notificaciones y en las consultas SQL no optimizadas.
    
- Flujo crítico: creación de evento → persistencia transaccional → generación de notificaciones → envío a usuarios.
    

---

### Estrategia de modernización y justificación

- **Desacoplamiento de UI y Backend**: extraer la capa de presentación como microservicio React independiente, comunicándose mediante APIs y eventos de dominio.
    
- **Strangler Fig Pattern**: coexistencia de monolito y microservicios durante la transición para minimizar riesgos.
    
- **Contenerización y Kubernetes**: despliegues automatizados, escalado horizontal y rollback sencillo.
    
- **Eventos Asíncronos con Kafka**: desacopla subprocesos de notificaciones y mejora resiliencia.
    

---

### Diagrama de componentes de la aplicación legacy

1. **Django Admin & Web UI**: Renderizado MVT monolítico.
    
2. **Vistas (Views)**: Lógicas de CRUD para eventos, asistentes y finanzas.
    
3. **ORM + Models**: Abstracción SQL para SQLite.
    
4. **Cola de Notificaciones**: RabbitMQ para email y SMS.
    
5. **SQLite DB**: Base de datos única sin concurrencia ni replicación.
    
6. **Integraciones Externas**: Pasarela de pagos, SMTP, proveedor SMS.
    

---

## Arquitectura “To-Be"

**Descripción general del diseño objetivo de la solución:**

- Plataforma de microservicios desacoplados en contenedores Docker, orquestados por Kubernetes.
    
- API Gateway (Kong o AWS API Gateway) como punto único de entrada, gestionando rutas, autenticación y rate limiting.
    
- Comunicación interna síncrona (gRPC/REST) y asíncrona (Apache Kafka) para resiliencia.
    
- Persistencia poliglota: PostgreSQL para transaccional, Elasticsearch para búsqueda avanzada, Redis para cache.
    
- Front-end desacoplado: SPA en React que consume APIs REST/gRPC-Web.
    
- Observabilidad completa: métricas con Prometheus, trazas distribuidas con OpenTelemetry y logs centralizados en ELK.
    

---

## Partes del pre-experimento (para recibir retroalimentación)

### Propósito

- Validar rendimiento y escalabilidad del nuevo microservicio de notificaciones bajo cargas tipo pico (1.000 eventos/s).
    
- Comprobar entrega fiable y ordenada de mensajes a través de Kafka.
    

### Requisitos

- Cluster de Kubernetes con al menos 3 nodos (staging).
    
- Cluster Kafka replicado para topics de notificaciones.
    
- Generadores de carga (k6, Gatling) configurados para simular tráfico real.
    

### Descripción

1. Desplegar la imagen Docker del microservicio de notificaciones en staging.
    
2. Publicar 1.000 eventos/s en el topic `event-notifications` de Kafka.
    
3. Monitorear latencia, tasa de errores y uso de CPU/RAM.
    
4. Ajustar réplicas y thread pools según métricas obtenidas.
    

---

_Actualiza rutas de diagramas e imágenes según repositorio de artefactos._