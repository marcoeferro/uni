# Usamos una imagen ligera de Python con Linux
FROM python:3.9-slim

# Actualiza e instala las dependencias necesarias (cron, tzdata)
RUN apt-get update && apt-get install -y tzdata cron && rm -rf /var/lib/apt/lists/*

# Establece el timezone (por ejemplo, America/Argentina/Buenos_Aires)
ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip a la última versión
RUN pip install --upgrade pip

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia el archivo de requerimientos
COPY requirements.txt ./

# Instala las dependencias del proyecto desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo principal y la carpeta src al contenedor
COPY main.py ./
COPY src ./

# Da permisos de ejecución al script main.py (si es necesario)
RUN chmod +x main.py

# Configura cron para ejecutar el script todos los días a las 09:04 AM
RUN echo "0 22 * * * /usr/local/bin/python3 /usr/src/app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mi_tarea_diaria

# Da permisos adecuados al archivo de cron
RUN chmod 0644 /etc/cron.d/mi_tarea_diaria

# Aplica el cron job
RUN crontab /etc/cron.d/mi_tarea_diaria

# Crea el archivo de log para cron
RUN touch /var/log/cron.log

# Comando que arranca cron en segundo plano y muestra los logs
CMD ["cron", "-f"]