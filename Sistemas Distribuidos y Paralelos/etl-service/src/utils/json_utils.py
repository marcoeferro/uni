
def json_traverser(dict_to_traverse: dict) -> dict:
    root_data = {}
    for k, v in dict_to_traverse.items():
        if isinstance(v, dict):
            root_data.update(json_traverser(v))
        else:
            root_data[k] = v
    return root_data

def get_values_by_keys(data: dict, keys: list) -> dict:
    return {key: data[key] for key in keys if key in data}