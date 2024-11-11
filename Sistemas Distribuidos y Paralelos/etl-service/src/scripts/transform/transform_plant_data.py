from pathlib import Path
from . import path_setup # This ensures the sys.path is modified
from utils.json_utils import get_values_by_keys, json_traverser
import json
import datetime

def transform_plant_data(file) -> json:

    # Define the base directory (e.g., the directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Define the raw data directory relative to the base directory
    raw_data_dir = base_dir/'..'/'..'/'..'/'data'/'raw'

    # Define the path to the raw plant JSON file
    raw_file_path = raw_data_dir / 'plant.json'


    # Define the raw data directory relative to the base directory
    processed_data_dir = base_dir/'..'/'..'/'..'/'data'/'processed'

    # Define the path to the processed plant_data JSON file
    processed_file_path = processed_data_dir / f'processed_plant_data_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    labels = ["accountName", "city", "coal", "co2", "country", "creatDate", "designCompany", "fixedPowerPrice", "flatPeriodPrice", "formulaCo2", "formulaCoal", "formulaMoney", "formulaTree", "gridCompany", "gridPort", "gridServerUrl", "id", "installMap", "isShare", "lat", "locationImg", "lng", "moneyUnit", "moneyUnitText", "nominalPower", "peakPeriodPrice", "plantImg", "plantName", "plantType", "protocolId", "tempType", "timezone", "tree", "valleyPeriodPrice", "eTotal"]


    
    data = file
    
    data_raw = json_traverser(data)
    data_cleaned = get_values_by_keys(data=data_raw,keys=labels)

    with processed_file_path.open('w') as outfile:
        json.dump(obj=data_cleaned,fp=outfile)
        return data_cleaned