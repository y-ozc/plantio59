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
    selected_items = list(user_vector.items())[1:5]  # Slice from second to fifth entry

    # Unzip keys and values
    _, weights = zip(*selected_items)  # Ignore names, keep weights
    
    # Pick a number from 1 to 4 using weights
    return random.choices(range(1, 5), weights=weights)

def get_categories(category):

    cultivars_data = load_cultivars()
    
    filtered_cultivars = [item for item in cultivars_data if item['category'] == category]
    
    return filtered_cultivars



def genRec(data):

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

    # Return the recommendation based on the user or a default message
    return json.dumps(user_plant_data) 



# !!! web app will interract with this function
# STUB
# Take user name and garden.
# Uses cultivars data to come up with 3 plant recommendations
def generateRecommendations(json_vector): #user vector will come as a json entry string

    # parse user vector
    try:
        user_vector = json.loads(json_vector)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    # store ideal eoc
    ideal_eoc = user_vector["eoc_ideal"]


    # randomly pick category based on user vector. 
    # the higher the catogry in the user vector, the more likely it is to be picked
    # do this 3 times

    alley = pick_category(user_vector)
    simple = pick_category(user_vector)
    challenge = pick_category(user_vector)

    # for cat alley
    # fetch all the plants in from the culitvars with that category
    possible_picks = get_categories(alley)

    # pick closest eocy
    alley_pick = min(possible_picks, key=lambda item: abs(item['value'] - ideal_eoc))

    # for cat simple
    # fetch all the plants in from the culitvars with that category
    possible_picks = get_categories(simple)

    # pick a little bit higher eoc 
    simple_pick = min(possible_picks, key=lambda item: abs(item['value'] - (ideal_eoc + 0.1)))

    # for cat challenge   
    # fetch all the plants in from the culitvars with that category
    possible_picks = get_categories(challenge)

    # pick a little bit lower eoc
    challenge_pick = min(possible_picks, key=lambda item: abs(item['value'] - (ideal_eoc - 0.1)))

    # cobine all picks into a single 
    combined_result = [alley_pick, simple_pick, challenge_pick]

    # Convert to JSON string for easy transmission to JavaScript
    return json.dumps(combined_result)





