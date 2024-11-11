from pathlib import Path
import requests
import json
import sqlite3
from datetime import datetime, timedelta
# Data Extractors
from src.scripts.extract.login import login
from src.scripts.extract.extract_batery_info_chart_data import get_batery_info_chart_data
from src.scripts.extract.extract_energy_area_chart_data import data_energy_area_chart_data
from src.scripts.extract.extract_photovoltaic_device_data import get_photovoltaic_device_data
from src.scripts.extract.extract_plant_data import get_plant_data
from src.scripts.extract.extract_storage_status_data import get_storage_status_data
from src.scripts.extract.extract_storage_total_data import get_storage_total_data
from src.scripts.extract.extract_wheater_data import get_wheater_data
# Data Cleaners
from src.scripts.transform.transform_batery_info import transform_batery_info
from src.scripts.transform.transform_energy_area_chart import transform_energy_area_chart
from src.scripts.transform.transform_photovoltaic_device import transform_photovoltaic_device
from src.scripts.transform.transform_plant_data import transform_plant_data
from src.scripts.transform.transform_storage_status_data import transform_storage_status_data
from src.scripts.transform.transform_storage_total_data import transform_storage_total_data
from src.scripts.transform.transform_wheater import transform_wheater
# Data Loaders
from src.scripts.load.loader_batery_charge_discharge import create_battery_charge_discharge_table, insert_battery_charge_discharge
from src.scripts.load.loader_batery_soc_info import create_battery_soc_info_table, insert_battery_soc_info
from src.scripts.load.loader_energy_area_chart import create_energy_area_chart_table, insert_energy_area_chart
from src.scripts.load.loader_energy_storage_day import create_energy_storage_day_table, insert_energy_storage_day
from src.scripts.load.loader_photovoltaic_device import create_device_data_table, insert_device_data
from src.scripts.load.loader_plant_data import create_plant_table, insert_plant
from src.scripts.load.loader_storage_status import create_storage_status_table, insert_storage_status
from src.scripts.load.loader_storage_total_data import create_storage_total_table, insert_storage_total
from src.scripts.load.loader_wheater import create_wheater_table,insert_wheater


def run_etl() ->None:
    db_path = Path(__file__).parent /'..'/'scrapped_data.db'
    print(f"PATH {db_path}")
    conn = sqlite3.connect(db_path)

    loginUrl = "https://server.growatt.com/login"

    session = requests.session()

    # Extracting Data
    login(loginUrl,session=session)

    batery_info = get_batery_info_chart_data(session=session, loginUrl=loginUrl)
    energy_area_chart = data_energy_area_chart_data(session=session, loginUrl=loginUrl)
    photovoltaic_device = get_photovoltaic_device_data(session=session, loginUrl=loginUrl)
    plant_data = get_plant_data(session=session, loginUrl=loginUrl)
    storage_status = get_storage_status_data(session=session, loginUrl=loginUrl)
    storage_total = get_storage_total_data(session=session, loginUrl=loginUrl)
    wheater = get_wheater_data(session=session, loginUrl=loginUrl)

    # TRANSFORMING AND LOADING DATA

    # Define the base directory (e.g., the directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Define the data directory relative to the base directory
    data_dir = base_dir / 'data' / 'raw'

    # Ensure the directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    # Define the path to the batery_info JSON file
    file_path = data_dir / f'raw_batery_info_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(batery_info!=None):
            outfile.write(json.dumps(batery_info))
            data_cleaned = transform_batery_info(batery_info)
            create_battery_charge_discharge_table(conn)
            create_battery_soc_info_table(conn)
            for items in zip(data_cleaned["cdsTitle"],data_cleaned["cd_charge"],data_cleaned["cd_disCharge"]) :
                insert_battery_charge_discharge(connection=conn,timestamp=items[0],charge=items[1],discharge=items[2])
            
            date_time = datetime.strptime(data_cleaned["date"], "%Y-%m-%d")
            
            for item in data_cleaned["capacity"]:
                insert_battery_soc_info(connection=conn,timestamp=date_time,percentage=item)
                date_time += timedelta(minutes=5)
        else:
            print("ERROR the batery_info data is NULL")

    # Define the path to the energy_area_chart JSON file
    file_path = data_dir / f'raw_energy_area_chart_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(energy_area_chart!=None):
            outfile.write(json.dumps(energy_area_chart))
            data_cleaned = transform_energy_area_chart(energy_area_chart)
            create_energy_area_chart_table(connection=conn)
            create_energy_storage_day_table(connection=conn)
            
            date_time = datetime.now()
            for item in zip(data_cleaned["pacToGrid"],data_cleaned["ppv"],data_cleaned["sysOut"],data_cleaned["userLoad"],data_cleaned["pacToUser"]):
                insert_energy_area_chart(connection=conn,timestamp=date_time,pacToGrid=item[0],ppv=item[1],sysOut=item[2],userLoad=item[3],pacToUser=item[4])
                date_time += timedelta(minutes=5)

            insert_energy_storage_day(
                connection=conn,
                timestamp=datetime.now(),
                eChargeTotal = data_cleaned["eChargeTotal"],
                eAcDisCharge = data_cleaned["eAcDisCharge"],
                eDisCharge = data_cleaned["eDisCharge"],
                eCharge = data_cleaned["eCharge"],
                eAcCharge = data_cleaned["eAcCharge"],
                eDisChargeTotal = data_cleaned["eDisChargeTotal"])
        else:
            print("ERROR the energy_area_chart data is NULL")

    # Define the path to the photovoltaic_device JSON file
    file_path = data_dir / f'raw_photovoltaic_device_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(photovoltaic_device!=None):
            outfile.write(json.dumps(photovoltaic_device))
            data_cleaned = transform_photovoltaic_device(photovoltaic_device)
            create_device_data_table(conn)
            insert_device_data(connection=conn,timestamp=datetime.now(),
                                accountName = data_cleaned["accountName"],
                                alias = data_cleaned["alias"],
                                bdcStatus = data_cleaned["bdcStatus"],
                                datalogSn = data_cleaned["datalogSn"],
                                datalogTypeTest = data_cleaned["datalogTypeTest"],
                                deviceModel = data_cleaned["deviceModel"],
                                deviceType = data_cleaned["deviceType"],
                                deviceTypeName = data_cleaned["deviceTypeName"],
                                eMonth = data_cleaned["eMonth"],
                                eToday = data_cleaned["eToday"],
                                eTotal = data_cleaned["eTotal"],
                                lastUpdateTime = data_cleaned["lastUpdateTime"],
                                location = data_cleaned["location"],
                                nominalPower = data_cleaned["nominalPower"],
                                pac = data_cleaned["pac"],
                                plantId = data_cleaned["plantId"],
                                plantName = data_cleaned["plantName"],
                                ptoStatus = data_cleaned["ptoStatus"],
                                sn = data_cleaned["sn"],
                                status = data_cleaned["status"],
                                timeServer = data_cleaned["timeServer"],
                                timezone = data_cleaned["timezone"])
        else:
            print("ERROR the photovoltaic_device data is NULL")

    # Define the path to the plant_data JSON file
    file_path = data_dir / f'raw_plant_data_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(plant_data!=None):
            outfile.write(json.dumps(plant_data))
            data_cleaned = transform_plant_data(plant_data)
            create_plant_table(conn)
            insert_plant(connection=conn,
                        timestamp=datetime.now(),
                        accountName = data_cleaned["accountName"],
                        city = data_cleaned["city"],
                        coal = data_cleaned["coal"],
                        co2 = data_cleaned["co2"],
                        country = data_cleaned["country"],
                        creatDate = data_cleaned["creatDate"],
                        designCompany = data_cleaned["designCompany"],
                        fixedPowerPrice = data_cleaned["fixedPowerPrice"],
                        flatPeriodPrice = data_cleaned["flatPeriodPrice"],
                        formulaCo2 = data_cleaned["formulaCo2"],
                        formulaCoal = data_cleaned["formulaCoal"],
                        formulaMoney = data_cleaned["formulaMoney"],
                        formulaTree = data_cleaned["formulaTree"],
                        gridCompany = data_cleaned["gridCompany"],
                        gridPort = data_cleaned["gridPort"],
                        gridServerUrl = data_cleaned["gridServerUrl"],
                        id = data_cleaned["id"],
                        installMap = data_cleaned["installMap"],
                        isShare = data_cleaned["isShare"],
                        lat = data_cleaned["lat"],
                        locationImg = data_cleaned["locationImg"],
                        lng = data_cleaned["lng"],
                        moneyUnit = data_cleaned["moneyUnit"],
                        moneyUnitText = data_cleaned["moneyUnitText"],
                        nominalPower = data_cleaned["nominalPower"],
                        peakPeriodPrice = data_cleaned["peakPeriodPrice"],
                        plantImg = data_cleaned["plantImg"],
                        plantName = data_cleaned["plantName"],
                        plantType = data_cleaned["plantType"],
                        protocolId = data_cleaned["protocolId"],
                        tempType = data_cleaned["tempType"],
                        timezone = data_cleaned["timezone"],
                        tree = data_cleaned["tree"],
                        valleyPeriodPrice = data_cleaned["valleyPeriodPrice"],
                        eTotal = data_cleaned["eTotal"])
        else:
            print("ERROR the plant_data data is NULL")

    # Define the path to the storage_status JSON file
    file_path = data_dir / f'raw_storage_status_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(storage_status!=None):
            outfile.write(json.dumps(storage_status))
            data_cleaned = transform_storage_status_data(storage_status)
            create_storage_status_table(conn)
            insert_storage_status(connection=conn, 
                                    timestamp=datetime.now(),
                                    batPower = data_cleaned["batPower"],
                                    capacity = data_cleaned["capacity"],
                                    deviceType = data_cleaned["deviceType"],
                                    fAcInput = data_cleaned["fAcInput"],
                                    fAcOutput = data_cleaned["fAcOutput"],
                                    gridPower = data_cleaned["gridPower"],
                                    iPv1 = data_cleaned["iPv1"],
                                    iPv2 = data_cleaned["iPv2"],
                                    iTotal = data_cleaned["iTotal"],
                                    invStatus = data_cleaned["invStatus"],
                                    loadPower = data_cleaned["loadPower"],
                                    loadPrecent = data_cleaned["loadPrecent"],
                                    panelPower = data_cleaned["panelPower"],
                                    ppv1 = data_cleaned["ppv1"],
                                    ppv2 = data_cleaned["ppv2"],
                                    rateVA = data_cleaned["rateVA"],
                                    status = data_cleaned["status"],
                                    vAcInput = data_cleaned["vAcInput"],
                                    vAcOutput = data_cleaned["vAcOutput"],
                                    vBat = data_cleaned["vBat"],
                                    vPv1 = data_cleaned["vPv1"],
                                    vPv2 = data_cleaned["vPv2"])
        else:
            print("ERROR the storage_status data is NULL")

    # Define the path to the storage_total JSON file
    file_path = data_dir / f'raw_storage_total_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(storage_total!=None):
            outfile.write(json.dumps(storage_total))
            data_cleaned = transform_storage_total_data(storage_total)
            create_storage_total_table(connection=conn)
            insert_storage_total(connection=conn, 
                                    timestamp=datetime.now(),
                                    chargeToday = data_cleaned["chargeToday"],
                                    chargeTotal = data_cleaned["chargeTotal"],
                                    deviceType = data_cleaned["deviceType"],
                                    eDischargeToday = data_cleaned["eDischargeToday"],
                                    eDischargeTotal = data_cleaned["eDischargeTotal"],
                                    eToGridToday = data_cleaned["eToGridToday"],
                                    eToGridTotal = data_cleaned["eToGridTotal"],
                                    eToUserToday = data_cleaned["eToUserToday"],
                                    eToUserTotal = data_cleaned["eToUserTotal"],
                                    epvToday = data_cleaned["epvToday"],
                                    epvTotal = data_cleaned["epvTotal"],
                                    useEnergyToday = data_cleaned["useEnergyToday"],
                                    useEnergyTotal = data_cleaned["useEnergyTotal"])
        else:
            print("ERROR the storage_total data is NULL")


    # Define the path to the wheater JSON file
    file_path = data_dir / f'raw_wheater_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    with file_path.open("w") as outfile:
        if(wheater!=None):
            outfile.write(json.dumps(wheater))
            data_cleaned = transform_wheater(wheater)
            create_wheater_table(connection=conn)
            insert_wheater(
                connection = conn,
                timestamp = datetime.now(),
                city = data_cleaned["city"],
                Week = data_cleaned["Week"],
                dataStr = data_cleaned["dataStr"],
                cloud = data_cleaned["cloud"],
                hum = data_cleaned["hum"],
                wind_deg = data_cleaned["wind_deg"],
                pres = data_cleaned["pres"],
                pcpn = data_cleaned["pcpn"],
                fl = data_cleaned["fl"],
                tmp = data_cleaned["tmp"],
                wind_sc = data_cleaned["wind_sc"],
                cond_txt = data_cleaned["cond_txt"],
                wind_dir = data_cleaned["wind_dir"],
                wind_spd = data_cleaned["wind_spd"],
                cond_code = data_cleaned["cond_code"],
                loc = data_cleaned["loc"],
                utc = data_cleaned["utc"],
                ss = data_cleaned["ss"],
                admin_area = data_cleaned["admin_area"],
                toDay = data_cleaned["toDay"],
                location = data_cleaned["location"],
                parent_city = data_cleaned["parent_city"],
                cnty = data_cleaned["cnty"],
                sr = data_cleaned["sr"],
                status = data_cleaned["status"],
                radiant = data_cleaned["radiant"],
                tempType = data_cleaned["tempType"])
        else:
            print("ERROR the discharging data is NULL")