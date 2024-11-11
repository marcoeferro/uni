from flask import Flask, jsonify, abort
import sqlite3
from pathlib import Path

app = Flask(__name__)
db_path = Path(__file__).parent/'..' /'scrapped_data.db'

# Función para conectarse a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acceder a las filas como diccionarios
    return conn

# Rutas existentes para obtener todos los datos de cada tabla
@app.route('/DeviceData', methods=['GET'])
def get_device_data():
    conn = get_db_connection()
    device_data = conn.execute('SELECT * FROM device_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in device_data])

@app.route('/EnergyAreaChart', methods=['GET'])
def get_energy_area_chart():
    conn = get_db_connection()
    energy_area_chart = conn.execute('SELECT * FROM anergy_area_chart').fetchall()
    conn.close()
    return jsonify([dict(row) for row in energy_area_chart])

@app.route('/EnergyStorageDay', methods=['GET'])
def get_energy_storage_day():
    conn = get_db_connection()
    energy_storage_day = conn.execute('SELECT * FROM energy_storage_day').fetchall()
    conn.close()
    return jsonify([dict(row) for row in energy_storage_day])

@app.route('/Plant', methods=['GET'])
def get_plant():
    conn = get_db_connection()
    plant = conn.execute('SELECT * FROM plant').fetchall()
    conn.close()
    return jsonify([dict(row) for row in plant])

@app.route('/StorageStatus', methods=['GET'])
def get_storage_status():
    conn = get_db_connection()
    storage_status = conn.execute('SELECT * FROM storage_status').fetchall()
    conn.close()
    return jsonify([dict(row) for row in storage_status])

@app.route('/StorageTotal', methods=['GET'])
def get_storage_total():
    conn = get_db_connection()
    storage_total = conn.execute('SELECT * FROM storage_total').fetchall()
    conn.close()
    return jsonify([dict(row) for row in storage_total])

@app.route('/Wheater', methods=['GET'])
def get_wheater():
    conn = get_db_connection()
    wheater = conn.execute('SELECT * FROM wheater').fetchall()
    conn.close()
    return jsonify([dict(row) for row in wheater])

@app.route('/BatteryCharge', methods=['GET'])
def get_battery_charge():
    conn = get_db_connection()
    battery_charge = conn.execute('SELECT * FROM battery_charge_discharge').fetchall()
    conn.close()
    return jsonify([dict(row) for row in battery_charge])

@app.route('/BatterySoc', methods=['GET'])
def get_battery_soc():
    conn = get_db_connection()
    battery_soc = conn.execute('SELECT * FROM battery_soc_info').fetchall()
    conn.close()
    return jsonify([dict(row) for row in battery_soc])

# Nuevas rutas para obtener datos por timestamp
@app.route('/DeviceData/<string:timestamp>', methods=['GET'])
def get_device_data_by_timestamp(timestamp):
    conn = get_db_connection()
    device_data = conn.execute('SELECT * FROM device_data WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if device_data is None:
        abort(404)  # Devuelve un error 404 si no se encuentra el timestamp
    return jsonify(dict(device_data))

@app.route('/EnergyAreaChart/<string:timestamp>', methods=['GET'])
def get_energy_area_chart_by_timestamp(timestamp):
    conn = get_db_connection()
    energy_area_chart = conn.execute('SELECT * FROM anergy_area_chart WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if energy_area_chart is None:
        abort(404)
    return jsonify(dict(energy_area_chart))

@app.route('/EnergyStorageDay/<string:timestamp>', methods=['GET'])
def get_energy_storage_day_by_timestamp(timestamp):
    conn = get_db_connection()
    energy_storage_day = conn.execute('SELECT * FROM energy_storage_day WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if energy_storage_day is None:
        abort(404)
    return jsonify(dict(energy_storage_day))

@app.route('/Plant/<string:timestamp>', methods=['GET'])
def get_plant_by_timestamp(timestamp):
    conn = get_db_connection()
    plant = conn.execute('SELECT * FROM plant WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if plant is None:
        abort(404)
    return jsonify(dict(plant))

@app.route('/StorageStatus/<string:timestamp>', methods=['GET'])
def get_storage_status_by_timestamp(timestamp):
    conn = get_db_connection()
    storage_status = conn.execute('SELECT * FROM storage_status WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if storage_status is None:
        abort(404)
    return jsonify(dict(storage_status))

@app.route('/StorageTotal/<string:timestamp>', methods=['GET'])
def get_storage_total_by_timestamp(timestamp):
    conn = get_db_connection()
    storage_total = conn.execute('SELECT * FROM storage_total WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if storage_total is None:
        abort(404)
    return jsonify(dict(storage_total))

@app.route('/Wheater/<string:timestamp>', methods=['GET'])
def get_wheater_by_timestamp(timestamp):
    conn = get_db_connection()
    wheater = conn.execute('SELECT * FROM wheater WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if wheater is None:
        abort(404)
    return jsonify(dict(wheater))

@app.route('/BatteryCharge/<string:timestamp>', methods=['GET'])
def get_battery_charge_by_timestamp(timestamp):
    conn = get_db_connection()
    battery_charge = conn.execute('SELECT * FROM battery_charge_discharge WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if battery_charge is None:
        abort(404)
    return jsonify(dict(battery_charge))

@app.route('/BatterySoc/<string:timestamp>', methods=['GET'])
def get_battery_soc_by_timestamp(timestamp):
    conn = get_db_connection()
    battery_soc = conn.execute('SELECT * FROM battery_soc_info WHERE timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if battery_soc is None:
        abort(404)
    return jsonify(dict(battery_soc))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
