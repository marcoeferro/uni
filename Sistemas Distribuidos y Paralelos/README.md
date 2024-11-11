# Proyecto de Microservicios para ETL, Scheduler y CRUD

## Tabla de Contenidos
1. [Descripción General del Proyecto](#descripción-general-del-proyecto)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Instalación y Configuración](#instalación-y-configuración)
   - [Requisitos Previos](#requisitos-previos)
   - [Clonar el Repositorio](#clonar-el-repositorio)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Uso de los Servicios](#uso-de-los-servicios)
   - [ETL Service](#etl-service)
   - [Scheduler Service](#scheduler-service)
   - [CRUD Service](#crud-service)
6. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
7. [Contribución](#contribución)
8. [Licencia](#licencia)

## Descripción General del Proyecto
Este proyecto consiste en un sistema de microservicios que facilita la extracción diaria de información de una página web para su posterior carga en una base de datos. Los datos pueden ser consumidos por clientes para visualizarlos en un dashboard. El sistema se compone de tres servicios principales:
1. **Scheduler:** Controla la periodicidad de las tareas de extracción y carga de datos.
2. **ETL (Extract, Transform, Load):** Se encarga de la extracción, transformación y carga de datos desde la fuente al almacenamiento.
3. **CRUD:** Proporciona una API RESTful para la gestión y consulta de los datos.

## Tecnologías Utilizadas
- **Python**: Para la lógica del backend.
- **SQLite**: Base de datos ligera utilizada para el almacenamiento local.
- **Flask**: Framework web para el desarrollo del API.
- **SQLAlchemy**: ORM para la interacción con la base de datos.
- **Apache Airflow**: Herramienta de programación y gestión de flujos de trabajo (Scheduler).
- **Docker**: Para la contenedorización de los servicios.

## Instalación y Configuración

### Requisitos Previos
Asegúrate de tener instalado:
- **Docker**: Requerido para ejecutar los servicios de manera aislada y reproducible.

### Clonar el Repositorio
Para obtener el código fuente y comenzar con el proyecto, sigue los siguientes pasos:

```bash
git clone https://github.com/marcoeferro/SistemasDistribuidos.git
cd SistemasDistribuidos
```

## Estructura del Proyecto
La estructura de carpetas de este proyecto es la siguiente:

```
/SistemasDistribuidos
├── /etl_service                # Servicio ETL
│   ├── main.py                 # Lógica del ETL
│   ├── requirements.txt        # Dependencias del servicio ETL
├── /scheduler_service          # Servicio Scheduler
│   ├── dag.py                  # Definición de flujos de trabajo en Airflow
│   ├── requirements.txt        # Dependencias del servicio Scheduler
├── /crud_service               # Servicio CRUD
│   ├── app.py                  # API RESTful para la gestión de datos
│   ├── models.py               # Definición de modelos de base de datos
│   ├── requirements.txt        # Dependencias del servicio CRUD
├── /docker                     # Archivos de configuración de Docker
│   ├── docker-compose.yml      # Orquestación de los servicios en contenedores
└── README.md                   # Documentación del proyecto
```

## Uso de los Servicios

### ETL Service
El **ETL Service** es ejecutado de forma automática por el Scheduler, extrayendo, transformando y cargando los datos diariamente. No requiere intervención manual.

### Scheduler Service
El **Scheduler Service** utiliza Apache Airflow para controlar las tareas ETL. Al iniciar su contenedor Docker, el servicio programará y gestionará la ejecución de las tareas.

### CRUD Service
El **CRUD Service** expone endpoints GET para consultar los datos procesados. La definición exacta de los endpoints estará disponible en futuras actualizaciones.

## Arquitectura del Proyecto
El proyecto utiliza una arquitectura basada en microservicios, donde cada servicio (ETL, Scheduler, CRUD) está contenedorizado usando Docker. Kubernetes o Docker Compose pueden utilizarse para orquestar los contenedores y facilitar la comunicación entre los servicios.

La arquitectura permite:
- **Escalabilidad**: Los microservicios pueden escalar de manera independiente.
- **Mantenimiento**: Los servicios pueden ser actualizados o reemplazados sin afectar a otros.
- **Despliegue**: Docker garantiza que los servicios se ejecuten de manera consistente en cualquier entorno.

## Contribución
Las contribuciones a este proyecto son bienvenidas. Para contribuir, sigue los pasos a continuación:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad o corrección (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request explicando los cambios realizados. Aquí tienes un [video tutorial sobre cómo hacer un Pull Request](https://youtu.be/BPns9r76vSI).

## Licencia
Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo de licencia o haz clic en el siguiente enlace:

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)