
"""
## Grafico de SOC (state of charge)

Eje y : Valores de 0% a 125% con incrementos de 25%

Eje x : horas desde 00:00 hs hasta 16:40 hs con aumentos de 02:05hs

Grafo : a % value for every 5 minutes for a period of time of 24 hs (all this data goes for the same day  the day of the request)

### Grafico de SOC (state of charge)
```
|      timestamp      | percentage |
|---------------------|------------|
| 2024-10-05 00:00:00 |    45.0    | 
| 2024-10-05 00:05:00 |    47.5    |
| 2024-10-05 00:10:00 |    50.0    |
| ...                 |    ...     |
| 2024-10-05 23:55:00 |    42.0    |
```
"""
def create_battery_soc_info_table(connection):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battery_soc_info (
                timestamp TEXT PRIMARY KEY,
                percentage REAL  
            )
        ''')
        conn.commit()

def insert_battery_soc_info(connection,timestamp, percentage):
    with connection as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO battery_soc_info (timestamp, percentage) 
                VALUES (?, ?)
            ''', (timestamp, percentage))
            conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting batery SOC data: {e}")