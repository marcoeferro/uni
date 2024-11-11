from pathlib import Path
import json
from . import path_setup # This ensures the sys.path is modified
from utils.json_utils import get_values_by_keys, json_traverser
import datetime
def transform_energy_area_chart(file) -> json:
    # Define the base directory (e.g., the directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Define the raw data directory relative to the base directory
    raw_data_dir = base_dir/'..'/'..'/'..'/'data'/'raw'

    # Define the path to the raw energy_area_chart JSON file
    raw_file_path = raw_data_dir / 'energy_area_chart.json'


    # Define the raw data directory relative to the base directory
    processed_data_dir = base_dir/'..'/'..'/'..'/'data'/'processed'

    # Define the path to the processed energy_area_chart JSON file
    processed_file_path = processed_data_dir / f'processed_energy_area_chart_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json'

    labels = ["eChargeTotal","pacToGrid","ppv","sysOut","userLoad","pacToUser","eAcDisCharge","eDisCharge","eCharge","eAcCharge","eDisChargeTotal"]

    
    data = file
    
    data_raw = json_traverser(data)
    data_cleaned = get_values_by_keys(data=data_raw,keys=labels)

    with processed_file_path.open('w') as outfile:
        json.dump(obj=data_cleaned,fp=outfile)
        return data_cleaned