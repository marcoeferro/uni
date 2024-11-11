# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.10.2

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your DAGs and scripts to the Airflow home directory
COPY dags/ $AIRFLOW_HOME/dags/
COPY scripts/ $AIRFLOW_HOME/scripts/

# Set the working directory
WORKDIR $AIRFLOW_HOME

# Set the entrypoint to the Airflow command
ENTRYPOINT ["airflow"]

# Default command to run the scheduler
CMD ["scheduler"]
