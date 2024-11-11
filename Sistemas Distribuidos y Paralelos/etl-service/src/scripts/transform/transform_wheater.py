from pathlib import Path
from . import path_setup # This ensures the sys.path is modified
from utils.json_utils import get_values_by_keys, json_traverser
import json
import datetime

def transform_wheater(file) -> json:

    # Define the base directory (e.g., the directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Define the raw data directory relative to the base directory
    raw_data_dir = base_dir/'..'/'..'/'..'/'data'/'raw'

    # Define the path to the raw wheater JSON file
    raw_file_path = raw_data_dir / 'wheater.json'


    # Define the raw data directory relative to the base directory
    processed_data_dir = base_dir/'..'/'..'/'..'/'data'/'processed'

    # Define the path to the processed wheater JSON file
    processed_file_path = processed_data_dir / f'processed_wheater_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    labels = ["Week","city","admin_area","cnty","location","parent_city","sr","ss","toDay","cloud","cond_code","cond_txt","fl","hum","pcpn","pres","tmp","wind_deg","wind_dir","wind_sc","wind_spd","status","loc","utc","dataStr","radiant","tempType"]

    
    data = file
    
    data_raw = json_traverser(data)
    data_raw.update(json_traverser(dict(data_raw["HeWeather6"][0])))
    data_cleaned = get_values_by_keys(data=data_raw,keys=labels)

    with processed_file_path.open('w') as outfile:
        json.dump(obj=data_cleaned,fp=outfile)
        return data_cleaned