import json
import os



JSON_PATH = os.path.join('data', 'user_vectors.json')

# STUB
# Takes a garden json and name. 
# Adjusts the base user vector accordingly.
# Saves it to user_vectors.json
def makeUserVector(garden_json, user_name):

    BASE_VECTOR = {
        "user": user_name,
        "ornament": 0.5,
        "herb": 0.5,
        "crop": 0.5,
        "mushroom": 0.5,
        "eoc_ideal": 0.5,
        "schedule": 1
    }

    # Ensure the directory exists before writing the file
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

    
    # Read the existing JSON data
    with open(JSON_PATH, "r") as file:
        try:
            data = json.load(file)  # Load existing JSON array
            if not isinstance(data, list):  # Ensure it's a list
                data = []
        except json.JSONDecodeError:  # Handle broken files
            data = []

    
    # Append the new entry
    data.append(BASE_VECTOR)

    # Write the updated array back to the file
    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)  # Pretty-print JSON

    return

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
    makeUserVector(os.path.join('data',' garden1.json'), 'new')
    makeUserVector(os.path.join('data',' garden2.json'), 'morgan')
    makeUserVector(os.path.join('data',' garden3.json'), 'alex')
    makeUserVector(os.path.join('data',' garden4.json'), 'reese')