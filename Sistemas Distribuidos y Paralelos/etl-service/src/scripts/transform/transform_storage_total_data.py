from pathlib import Path
from . import path_setup # This ensures the sys.path is modified
from utils.json_utils import get_values_by_keys, json_traverser
import json
import datetime

def transform_storage_total_data(file) -> json:
    # Define the base directory (e.g., the directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Define the raw data directory relative to the base directory
    raw_data_dir = base_dir/'..'/'..'/'..'/'data'/'raw'

    # Define the path to the raw storage_total_data JSON file
    raw_file_path = raw_data_dir / 'storage_total_data.json'


    # Define the raw data directory relative to the base directory
    processed_data_dir = base_dir/'..'/'..'/'..'/'data'/'processed'

    # Define the path to the processed storage_total_data JSON file
    processed_file_path = processed_data_dir / f'processed_storage_total_data_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    labels = ["chargeToday","chargeTotal","deviceType","eDischargeToday","eDischargeTotal","eToGridToday","eToGridTotal","eToUserToday","eToUserTotal","epvToday","epvTotal","useEnergyToday","useEnergyTotal"]

    
    data = file
    
    data_raw = json_traverser(data)
    data_cleaned = get_values_by_keys(data=data_raw,keys=labels)

    with processed_file_path.open('w') as outfile:
        json.dump(obj=data_cleaned,fp=outfile)
        return data_cleaned