
"""
### Explanation of Data Fields

**country**: The country where the plant is located (e.g., Argentina).

**formulaCo2**: CO2 emission formula value.

**accountName**: The name of the account associated with the plant.

**city**: The city where the plant is located (e.g., Villa Mercedes).

**timezone**: The timezone offset from UTC.

**co2**: Total CO2 emissions (in kg or another unit).

**gridCompany**: The company providing grid services (null if not applicable).

**creatDate**: The creation date of the plant record.

**formulaCoal**: Coal emission formula value.

**gridPort**: The port used for grid connection (null if not applicable).

**designCompany**: The company that designed the plant.

**fixedPowerPrice**: Fixed price of power (in the specified currency).

**id**: Unique identifier for the plant.

**lat**: Latitude of the plant location.

**valleyPeriodPrice**: Power price during valley periods (in the specified currency).

**tempType**: Temperature type (e.g., 0 might indicate a specific type).

**lng**: Longitude of the plant location.

**locationImg**: Image URL of the plant location.

**tree**: Number of trees equivalent to the CO2 offset.

**peakPeriodPrice**: Power price during peak periods (in the specified currency).

**installMap**: Installation map URL.

**plantType**: Type of plant (e.g., 0 might indicate a specific type).

**nominalPower**: Nominal power capacity of the plant (in watts).

**formulaMoney**: Money formula value.

**formulaTree**: Tree formula value.

**flatPeriodPrice**: Power price during flat periods (in the specified currency).

**eTotal**: Total energy generated or consumed over the plant's lifetime (in kWh).

**protocolId**: Protocol identifier.

**plantImg**: Image URL of the plant.

**isShare**: Indicates if the plant data is shared (true or false).

**gridServerUrl**: URL of the grid server (null if not applicable).

**coal**: Total coal consumption (in kg or another unit).

**moneyUnit**: Unit of currency (e.g., dollar).

**plantName**: Name of the plant.

**moneyUnitText**: Text representation of the currency unit (e.g., ¥).
"""
def create_plant_table(connection):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plant (
                timestamp TEXT PRIMARY KEY,
                accountName TEXT,
                city TEXT,
                coal REAL,
                co2 REAL,
                country TEXT,
                creatDate TEXT,
                designCompany TEXT,
                fixedPowerPrice REAL,
                flatPeriodPrice REAL,
                formulaCo2 REAL,
                formulaCoal REAL,
                formulaMoney REAL,
                formulaTree REAL,
                gridCompany TEXT,
                gridPort TEXT,
                gridServerUrl TEXT,
                id INTEGER,
                installMap TEXT,
                isShare TEXT,
                lat REAL,
                locationImg TEXT,
                lng REAL,
                moneyUnit TEXT,
                moneyUnitText TEXT,
                nominalPower REAL,
                peakPeriodPrice REAL,
                plantImg TEXT,
                plantName TEXT,
                plantType INTEGER,
                protocolId TEXT,
                tempType INTEGER,
                timezone REAL,
                tree INTEGER,
                valleyPeriodPrice REAL,
                eTotal REAL
            )
        ''')
        conn.commit()

def insert_plant(connection,timestamp,accountName,city,coal,co2,country,creatDate,designCompany,fixedPowerPrice,flatPeriodPrice,formulaCo2,formulaCoal,formulaMoney,formulaTree,gridCompany,gridPort,gridServerUrl,id,installMap,isShare,lat,locationImg,lng,moneyUnit,moneyUnitText,nominalPower,peakPeriodPrice,plantImg,plantName,plantType,protocolId,tempType,timezone,tree,valleyPeriodPrice,
eTotal):
    with connection as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO plant (timestamp,accountName,city,coal,co2,country,creatDate,designCompany,fixedPowerPrice,flatPeriodPrice,formulaCo2,formulaCoal,formulaMoney,formulaTree,gridCompany,gridPort,gridServerUrl,id,installMap,isShare,lat,locationImg,lng,moneyUnit,moneyUnitText,nominalPower,peakPeriodPrice,plantImg,plantName,plantType,protocolId,tempType,timezone,tree,valleyPeriodPrice,eTotal) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp,accountName,city,coal,co2,country,creatDate,designCompany,fixedPowerPrice,flatPeriodPrice,formulaCo2,formulaCoal,formulaMoney,formulaTree,gridCompany,gridPort,gridServerUrl,id,installMap,isShare,lat,locationImg,lng,moneyUnit,moneyUnitText,nominalPower,peakPeriodPrice,plantImg,plantName,plantType,protocolId,tempType,timezone,tree,valleyPeriodPrice,eTotal))
            conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting Plant data: {e}")