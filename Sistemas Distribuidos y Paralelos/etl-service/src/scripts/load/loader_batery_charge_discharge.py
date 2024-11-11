
"""
# Batery Info

## Grafico de carga y descarga 

Eje y : Valores de 0 Kwh a 20Kwh con incrementos de 5 Kwh

Eje x : Dias 


### Grafo : Charging  and Dischargin values en Kwh
```
|    date    | charge | discharge | 
|------------|--------|-----------|
| 2024-10-05 |  14.4  |    0.0    |
| 2024-10-06 |  14.4  |    0.0    |
| 2024-10-07 |  14.4  |    0.0    |
| 2024-10-08 |  14.4  |    0.0    |
| 2024-10-09 |  14.4  |    0.0    |
| 2024-10-10 |  14.4  |    0.0    |
| 2024-10-11 |  14.4  |    0.0    |
```

"""
def create_battery_charge_discharge_table(connection):
    """
    Creates the 'battery_charge_discharge' table in the database if it does not already exist.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.

    The table has the following columns:
        - timestamp (TEXT): The primary key representing the timestamp of the record.
        - charge (REAL): The charge value.
        - discharge (REAL): The discharge value.
    """
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battery_charge_discharge (
                timestamp TEXT PRIMARY KEY,
                charge REAL  ,
                discharge REAL  
            )
        ''')
        conn.commit()

def insert_battery_charge_discharge(connection, timestamp, charge, discharge):
    """
    Inserts a new record into the 'battery_charge_discharge' table.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        timestamp (str): The timestamp of the record.
        charge (float): The charge value.
        discharge (float): The discharge value.
    """
    with connection as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO battery_charge_discharge (timestamp, charge, discharge)
                VALUES (?, ?, ?)
            ''', (timestamp, charge, discharge))
            conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting Batery Charge Discharge data: {e}")
