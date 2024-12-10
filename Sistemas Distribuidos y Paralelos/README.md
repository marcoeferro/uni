# Proyecto de Microservicios para ETL, Scheduler y CRUD

## Tabla de Contenidos
1. [Descripción General del Proyecto](#descripción-general-del-proyecto)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Instalación y Configuración](#instalación-y-configuración)
   - [Requisitos Previos](#requisitos-previos)
   - [Clonar el Repositorio](#clonar-el-repositorio)
   - [Instalacion de Dependecias](#instalacion-de-dependencias)
      - [ETL Service](#etl-service)
      - [CRUD Service](#crud-service)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Uso de los Servicios](#uso-de-los-servicios)
   - [ETL Service](#etl-service)
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
- **Requests**: Libreria de python para realizar requests a APIs.

## Instalación y Configuración

### Requisitos Previos
Asegúrate de tener instalado:
- **Python**: Requerido para ejecutar los servicios.

### Clonar el Repositorio
Para obtener el código fuente y comenzar con el proyecto, sigue los siguientes pasos:

```bash
git clone https://github.com/marcoeferro/SistemasDistribuidos.git
cd SistemasDistribuidos
```
### instalacion de Dependencias
Para los instalar las dependencias asegurate de estar en la carpeta SistemasDistribuidos
#### ETL Service
Para el **ETL Service** Sigue los siguientes pasos:
Para Windows en cmd
```bash
cd elt-service
python -m venv venv 
.\venv\Scrips\activate.bat
pip install -r requirements.txt
```

#### CRUD Service
Para el **CRUD Service**  Sigue los siguientes pasos:
Para Windows en cmd
```bash
cd CRUD-service
python -m venv venv 
.\venv\Scrips\activate.bat
pip install -r requirements.txt
```

## Estructura del Proyecto
La estructura de carpetas de este proyecto es la siguiente:

```
/SistemasDistribuidos
├── /etl-service                # Servicio ETL
│   ├── main.py                 # Lógica del ETL
│   ├── requirements.txt        # Dependencias del servicio ETL
├── /scheduler-service          # Servicio Scheduler
│   ├── dag.py                  # Definición de flujos de trabajo en Airflow
│   ├── requirements.txt        # Dependencias del servicio Scheduler
├── /CRUD-service               # Servicio CRUD
│   ├── app.py                  # API RESTful para la gestión de datos
│   ├── models.py               # Definición de modelos de base de datos
│   ├── requirements.txt        # Dependencias del servicio CRUD
├── /docker                     # Archivos de configuración de Docker
├── docker-compose.yml          # Orquestación de los servicios en contenedores
├── LICENSE                     # Licencia MIT 
├── scrapped_data.db            # Base de dato que contiene los datos escrapeados
└── README.md                   # Documentación del proyecto
```

## Uso de los Servicios

### ETL Service
Para ejecutar el **ETL Service** Sigue los siguientes pasos una vez que te encuentres en la carpeta de SistemasDistribuidos
Para Windows en cmd
```bash
cd SistemasDistribuidos
cd elt-service
python run_etl_loop.py
```

### Scheduler Service
Fuera de servicio.

### CRUD Service
Para ejecutar el **CRUD Service**  Sigue los siguientes pasos una vez que te encuentres en la carpeta de SIstemasDistribuidos
Para Windows en cmd
```bash
cd SistemasDistribuidos
cd CRUD-service
python app.py
```
luego de esto deberas entrar a la direccion que aparece en la consola y a los endpoints correspondientes

## Arquitectura del Proyecto
`disclaimer` : el proycto como se describe en este readme aun no esta finalizado por lo que existen partes de esta arquietectura que no estan disponibles.
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