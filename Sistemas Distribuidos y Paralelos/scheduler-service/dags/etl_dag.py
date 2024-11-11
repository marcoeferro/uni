from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import os

# Definir la ruta del script main.py
ETL_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'etl-service', 'main.py')

# Definir la función que se ejecutará
def run_etl_script():
    # Ejecutar el script main.py
    subprocess.run([sys.executable, ETL_SCRIPT_PATH], check=True)

# Configuración del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 7),  # Ajusta esta fecha según necesites
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_dag',
    default_args=default_args,
    schedule_interval='@daily',  # Ejecutar una vez al día
    catchup=False,
) as dag:
    
    run_etl = PythonOperator(
        task_id='run_etl_script',
        python_callable=run_etl_script,
    )

    run_etl
