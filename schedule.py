import json
import os
import random


def load_cultivars():
    # Get the path to the JSON file (relative path)
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'cultivars_data.json')

    # Read the JSON file and return it as a Python object (list, dictionary, etc.)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data  # Return the data loaded from the JSON file
    except FileNotFoundError:
        print("data\cultivars_data.json file not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return None


def pick_category(user_vector):
    # Get categories
    selected_items = list(user_vector.items())[7:10]  # Slice from seventh to tenth entry

    # Unzip keys and values
    _, weights = zip(*selected_items)  # Ignore names, keep weights

    # Pick a number from 1 to 4 using weights
    return random.choices(range(1, 5), weights=weights)