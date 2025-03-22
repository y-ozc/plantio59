import json
import os
import math



JSON_PATH = "plantio59\\data\\user_vectors.json"

def load_info(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# STUB
# Takes a garden json and name. 
# Adjusts the base user vector accordingly.
# Saves it to user_vectors.json
def makeUserVector(garden_json_path, user_name, cultivar_info):
    # Load garden JSON data
    garden_json = load_info(garden_json_path)

    # Initialize base vector
    BASE_VECTOR = {
        "user": user_name,
        "ornament": 0.5,
        "herb": 0.5,
        "crop": 0.5,
        "mushroom": 0.5,
        "eoc_ideal": 0.5,
        "schedule": 1
    }

    # Create a dictionary to store category counts (categories 1-4)
    category_count = {1: 0, 2: 0, 3: 0, 4: 0}

    # Create a dictionary from info_json for fast lookup
    info_dict = {plant['cultivarName']: plant for plant in cultivar_info}

    # Iterate over the plants in the garden JSON
    for plant in garden_json:
        cultivar = plant.get('cultivar')

        # Check if the cultivar exists in the information JSON
        if cultivar in info_dict:
            plant_info = info_dict[cultivar]

            # Get the category of the plant from the info json and tally it
            category = plant_info['category']
            if category in category_count:
                category_count[category] += 1

    # Print category tallies
    print("Category tallies:")
    for category, count in category_count.items():
        print(f"Category {category}: {count}")

    # Adjust BASE_VECTOR based on category ranking
    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)
    category_names = ["ornament", "herb", "crop", "mushroom"]
    points = [0.4, 0.3, 0.2, 0.1]

    for i, (category, tally) in enumerate(sorted_categories):
        if tally > 0:
            BASE_VECTOR[category_names[category - 1]] += points[i]

    # Ensure the directory exists before writing the file
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

    # Read the existing JSON data
    try:
        with open(JSON_PATH, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (json.JSONDecodeError, FileNotFoundError):  # Handle empty/missing file
        data = []

    # Append the updated BASE_VECTOR
    data.append(BASE_VECTOR)

    # Write the updated array back to the file
    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)

    return


def calculate_ideal_eoc(garden_json_path, cultivar_info, decay_rate=0.2):
    
    garden_json = load_info(garden_json_path)

    # Create a dictionary for fast lookup of cultivar information
    info_dict = {plant['cultivarName']: plant for plant in cultivar_info}

    weighted_sum = 0
    total_weight = 0
    num_plants = len(garden_json)

    for index, plant in enumerate(garden_json):
        cultivar = plant.get('cultivar')

        if cultivar in info_dict:
            plant_info = info_dict[cultivar]
            eoc = float(plant_info.get('EOC', 0))  # Get EOC, default to 0 if missing
            
            # Exponential decay where newer plants have more weight
            weight = math.exp(-decay_rate * (num_plants - index - 1))  
            weighted_sum += eoc * weight
            total_weight += weight

    # Compute the weighted average
    ideal_eoc = weighted_sum / total_weight if total_weight > 0 else 0

    print(f"Ideal EOC for the garden: {ideal_eoc:.2f}")
    return ideal_eoc

# STUB 
# Fills in the parts of he user model concerning task functionality 
def makeUserScheduleModel():
    return

# !!! web app will interact with this function
# STUB
# updates user model based on one interaction and return the updated vector back
def updateVector(vecotor):
    return vecotor


if __name__ == "__main__":
    cultivar_info = load_info("plantio59\\data\\cultivars_data.json")
    # makeUserVector("plantio59\\data\\garden1.json", 'new', cultivar_info)
    # makeUserVector("plantio59\\data\\garden2.json", 'morgan', cultivar_info)
    # makeUserVector("plantio59\\data\\garden3.json", 'alex', cultivar_info)
    # # makeUserVector("plantio59\\data\\garden4.json", 'reese', cultivar_info)
    # print("Garden 2")
    # calculate_ideal_eoc("plantio59\\data\\garden2.json", cultivar_info, decay_rate=0.2)
    # print("Garden 3")
    # calculate_ideal_eoc("plantio59\\data\\garden3.json", cultivar_info, decay_rate=0.2)
    # print("Garden 4")
    # calculate_ideal_eoc("plantio59\\data\\garden4.json", cultivar_info, decay_rate=0.2)