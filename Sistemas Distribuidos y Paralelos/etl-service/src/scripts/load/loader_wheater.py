"""
### Explanation of Data Fields
1. **city**: The city where the weather data is being recorded (e.g., Villa Mercedes).
2. **Week**: The day of the Week (e.g., Saturday).
3. **dataStr**: A JSON string containing detailed weather information.
4. **data**: A structured JSON object containing detailed weather information.
   - **HeWeather6**: An array containing weather data.
     - **now**: Current weather conditions.
       - **cloud**: Cloud cover percentage.
       - **hum**: Humidity percentage.
       - **wind_deg**: Wind direction in degrees.
       - **pres**: Atmospheric pressure in hPa.
       - **pcpn**: Precipitation amount in mm.
       - **fl**: Feels like temperature in °C.
       - **tmp**: Actual temperature in °C.
       - **wind_sc**: Wind scale (Beaufort scale).
       - **cond_txt**: Weather condition text (e.g., Clear).
       - **wind_dir**: Wind direction (e.g., N for North).
       - **wind_spd**: Wind speed in km/h.
       - **cond_code**: Weather condition code.
     - **update**: Update times.
       - **loc**: Local update time.
       - **utc**: UTC update time.
     - **basic**: Basic location information.
       - **ss**: Sunset time.
       - **admin_area**: Administrative area (e.g., San Luis Province).
       - **toDay**: Today's date.
       - **location**: Location name (e.g., Villa Mercedes).
       - **parent_city**: Parent city (e.g., General Pedernera Department).
       - **cnty**: Country (e.g., Argentina).
       - **sr**: Sunrise time.
     - **status**: Status of the weather data (e.g., ok).
5. **radiant**: Radiant energy data (not provided in this case).
6. **tempType**: Temperature type (e.g., 0 might indicate Celsius).
"""
def create_wheater_table(connection):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wheater (
                timestamp TEXT PRIMARY KEY,
                city TEXT,
                Week TEXT,
                dataStr TEXT,
                cloud INTEGER,
                hum INTEGER,
                wind_deg INTEGER,
                pres INTEGER,
                pcpn REAL,
                fl REAL,
                tmp REAL,
                wind_sc INTEGER,
                cond_txt TEXT,
                wind_dir TEXT,
                wind_spd INTEGER,
                cond_code INTEGER,
                loc TEXT,
                utc TEXT,
                ss TIME,
                admin_area TEXT,
                toDay TEXT,
                location TEXT,
                parent_city TEXT,
                cnty TEXT,
                sr TIME,
                status TEXT,
                radiant TEXT,
                tempType INTEGER
            )
        ''')
        conn.commit()

def insert_wheater(connection,timestamp,city,Week,dataStr,cloud,hum,wind_deg,pres,pcpn,fl,tmp,wind_sc,cond_txt,wind_dir,wind_spd,cond_code,loc,utc,ss,admin_area,toDay,location,parent_city,cnty,sr,status,radiant,tempType):
    with connection as conn:
        cursor = conn.cursor()
        try:
          cursor.execute('''
              INSERT INTO wheater (timestamp,city,Week,dataStr,cloud,hum,wind_deg,pres,pcpn,fl,tmp,wind_sc,cond_txt,wind_dir,wind_spd,cond_code,loc,utc,ss,admin_area,toDay,location,parent_city,cnty,sr,status,radiant,tempType) 
              VALUES ( ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (timestamp,city,Week,dataStr,cloud,hum,wind_deg,pres,pcpn,fl,tmp,wind_sc,cond_txt,wind_dir,wind_spd,cond_code,loc,utc,ss,admin_area,toDay,location,parent_city,cnty,sr,status,radiant,tempType))
          conn.commit()
        except Exception as e:
            # Log the error or handle it in a specific way
            print(f"Error inserting Wheater data: {e}")