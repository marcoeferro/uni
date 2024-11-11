
"""
### Explanation of Data Fields

**deviceType**: The type of device (e.g., 3 might correspond to a specific type of energy device or inverter).

**ptoStatus**: Status of the PTO (Power Take-Off) system.

**timeServer**: The timestamp from the server.

**accountName**: The name of the account associated with the device.

**timezone**: The timezone offset from UTC.

**plantId**: The unique identifier for the plant.

**deviceTypeName**: The name/type of the device (e.g., "storage").

**nominalPower**: The nominal power capacity of the device (in watts).

**bdcStatus**: Status of the BDC (Battery Discharge Controller).

**eToday**: Energy generated or consumed today (in kWh).

**eMonth**: Energy generated or consumed this month (in kWh).

**datalogTypeTest**: The type of datalogger used (e.g., "ShineWIFI-S").

**eTotal**: Total energy generated or consumed over the device's lifetime (in kWh).

**pac**: Power output (in watts).

**datalogSn**: Serial number of the datalogger.

**alias**: Alias name for the device.

**location**: Location of the device.

**deviceModel**: Model of the device.

**sn**: Serial number of the device.

**plantName**: Name of the plant.

**status**: General status code of the device.

**lastUpdateTime**: The last time the device data was updated.
"""
def create_device_data_table(connection):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_data (
                timestamp TEXT PRIMARY KEY,
                accountName TEXT,
                alias TEXT,
                bdcStatus INTEGER,
                datalogSn TEXT,
                datalogTypeTest TEXT,
                deviceModel TEXT,
                deviceType INTEGER,
                deviceTypeName TEXT,
                eMonth REAL,
                eToday REAL,
                eTotal REAL,
                lastUpdateTime TEXT,
                location TEXT,
                nominalPower REAL,
                pac REAL,
                plantId INTEGER,
                plantName TEXT,
                ptoStatus INTEGER,
                sn TEXT,
                status INTEGER,
                timeServer TEXT,
                timezone REAL
            )
        ''')
        conn.commit()

def insert_device_data(connection,timestamp,
                        accountName, alias, bdcStatus, datalogSn, datalogTypeTest, deviceModel, deviceType, deviceTypeName, eMonth, eToday, eTotal, lastUpdateTime, location, nominalPower, pac, plantId, plantName, ptoStatus, sn, status, timeServer,timezone):
    with connection as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO device_data (timestamp,accountName, alias, bdcStatus, datalogSn, datalogTypeTest, deviceModel, deviceType, deviceTypeName, eMonth, eToday, eTotal, lastUpdateTime, location, nominalPower, pac, plantId, plantName, ptoStatus, sn, status, timeServer,timezone) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp,accountName, alias, bdcStatus, datalogSn, datalogTypeTest, deviceModel, deviceType, deviceTypeName, eMonth, eToday, eTotal, lastUpdateTime, location, nominalPower, pac, plantId, plantName, ptoStatus, sn, status, timeServer,timezone))
            conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting Photovoltaic Device data: {e}")