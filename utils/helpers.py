import re

def get_value_from_path(data, path):
    """Gets a value from a nested dictionary using a dot-separated path."""
    keys = path.split('.')
    current = data
    for key in keys:
        match = re.match(r"(.*?)\[(\d+)\]", key)
        if match:
            list_name, index = match.groups()
            current = current.get(list_name, [])
            if isinstance(current, list) and len(current) > int(index):
                current = current[int(index)]
            else:
                return None
        elif isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None

    # If the final resolved value is a dictionary from a search result, extract the link
    if isinstance(current, dict) and 'link' in current:
        return current['link']
        
    return current
