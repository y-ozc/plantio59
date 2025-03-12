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
        print("data/cultivars_data.json file not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON")
        return None


def pick_category(user_vector):
    # Get categories (morning, afternoon, evening)
    selected_items = list(user_vector.items())[6:8]  # Slice to get morning, afternoon, evening scores

    # Unzip keys and values
    _, weights = zip(*selected_items)  # Ignore names, keep weights

    # Pick a number from 1 to 4 using weights
    return random.choices(range(1, 5), weights=weights)


def get_categories(category):
    cultivars_data = load_cultivars()

    # Filter cultivars by category
    filtered_cultivars = [item for item in cultivars_data if item['category'] == category]

    return filtered_cultivars


def getUser(data):
    # Check if the data contains 'user' key directly
    if isinstance(data, dict) and 'user' in data:
        user_name = data.get('user')  # Extract the 'user' key from the data
    else:
        return 'Invalid data structure'

    # Load the plant data
    plants_data = load_cultivars()

    if plants_data is None:
        return 'Error loading plant data'

    switch = {
        'new': 0,  # Index in plants.json for 'new'
        'morgan': 1,  # Index for 'morgan'
        'alex': 2,  # Index for 'alex'
        'reese': 3,  # Index for 'reese'
        'random': 4,  # Index for 'random'
    }

    # Get the index for the user or use a default if not found
    index = switch.get(user_name, None)

    if index is None or index >= len(plants_data):
        return 'User not found or invalid index'

    # Get the corresponding plant entry
    user_plant_data = plants_data[index]
    user_trypls = userTime(json.dumps(data))

    # Return the recommendation based on the user or a default message
    return json.dumps(user_trypls)

def findLast(data):
    # Check if the data contains 'user' key directly
    if isinstance(data, dict) and 'user' in data:
        user_name = data.get('user')  # Extract the 'user' key from the data
    else:
        return 'Invalid data structure'

    # Load the plant data
    plants_data = load_cultivars()

    if plants_data is None:
        return 'Error loading plant data'

    switch = {
        'new': 0,  # Index in plants.json for 'new'
        'morgan': 1,  # Index for 'morgan'
        'alex': 2,  # Index for 'alex'
        'reese': 3,  # Index for 'reese'
        'random': 4,  # Index for 'random'
    }

    # Get the index for the user or use a default if not found
    index = switch.get(user_name, None)

    if index is None or index >= len(plants_data):
        return 'User not found or invalid index'

    # Get the corresponding plant entry
    user_plant_data = plants_data[index]

    # Extract the last item of each section
    last_items = {}
    for section, items in user_plant_data.items():
        if isinstance(items, list):  # Check if the section contains a list of items
            if items:  # Ensure the list is not empty
                last_items[section] = items[-1]  # Get the last item in the section
            else:
                last_items[section] = None  # If the list is empty, set to None
        else:
            last_items[section] = items  # If it's not a list, keep the value as-is

    # Return the last items of each section
    return json.dumps(last_items)

def userTime(json_vector):
    # Parse user vector
    try:
        user_vector = json.loads(json_vector)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return json.dumps({"error": "Invalid JSON input"})

    # Extract morning, afternoon, and evening scores
    morning_score = user_vector.get("morning", 0)
    afternoon_score = user_vector.get("afternoon", 0)
    evening_score = user_vector.get("evening", 0)

    # Determine the time with the highest score
    time_scores = {
        "morning": morning_score,
        "afternoon": afternoon_score,
        "evening": evening_score,
    }
    max_time = max(time_scores, key=time_scores.get)  # Get the time with the highest score


    # Pick plants based on the highest time score
    if max_time == "morning":
        return "You are an morning person"
    elif max_time == "evening":
        return "You are an evening person"
    elif max_time == "afternoon":
        return "You are an afternoon person"
    else:
        return 4

def getMessage(categoryMessage):
    cultivars_data = load_cultivars()

    # Filter cultivars by category and extract the 'message' field
    cultivarMessages = [item['message'] for item in cultivars_data if item['category'] == categoryMessage]

    return cultivarMessages


# Example usage
if __name__ == "__main__":
    # Example user vector for testing
    user_vector = {
        "user": "new",
        "ornament": 0.5,
        "herb": 0.5,
        "crop": 0.5,
        "mushroom": 0.5,
        "eoc_ideal": 0.5,
        "morning": 1,
        "evening": 0,
        "afternoon": 0
    }

    # Call the function you want to test
    result = userTime(json.dumps(user_vector))
    print("Test Result:", result)