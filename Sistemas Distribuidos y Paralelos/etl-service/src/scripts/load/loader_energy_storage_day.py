
"""
### Explanation of Data Fields

**eChargeTotal**: Total energy charged to the battery over its lifetime (in kWh).

**eDisCharge**: Energy discharged from the battery (in kWh).

**eCharge**: Energy charged to the battery (in kWh).

**eAcCharge**: Energy charged to the battery from the AC source (in kWh).

**eDisChargeTotal**: Total energy discharged from the battery over its lifetime (in kWh).

|  timestamp  | eChargeTotal | eAcDisCharge | eDisCharge |  eCharge   |  eAcCharge | eDisChargeTotal |
|----------- -|-------------|---------------|------------|------------|------------|-----------------|
| 2024-10-05  |    45.0     |       0       |      0     |    1275    |    1360    |      1360       | 
| 2024-10-05  |    47.5     |       0       |      0     |    1275    |    1360    |      1360       |
| 2024-10-05  |    50.0     |       0       |      0     |    1275    |    1360    |      1360       |
|     ...     |    ...      |      ...      |     ...    |     ...    |    ...     |      ...        |
| 2024-10-05  |    42.0     |       0       |      0     |    1280    |    1380    |      1380       |

"""
def create_energy_storage_day_table(connection):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_storage_day (
                timestamp TEXT PRIMARY KEY,
                eChargeTotal REAL,
                eAcDisCharge REAL,
                eDisCharge REAL,
                eCharge REAL,
                eAcCharge REAL,
                eDisChargeTotal REAL
            )
        ''')
        conn.commit()

def insert_energy_storage_day(connection,timestamp,eChargeTotal,eAcDisCharge,eDisCharge,eCharge,eAcCharge,eDisChargeTotal):
    with connection as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO energy_storage_day (timestamp,eChargeTotal,eAcDisCharge,eDisCharge,eCharge,eAcCharge,eDisChargeTotal) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp,eChargeTotal,eAcDisCharge,eDisCharge,eCharge,eAcCharge,eDisChargeTotal))
            conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting Energy Storage data: {e}")