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


def idkwhatthisdoes(data):
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

def get_user_garden(user_name):
    # Map user names to their respective garden numbers
    garden_mapping = {
        'new': 0,  # Index in plants.json for 'new'
        'morgan': 1,  # Index for 'morgan'
        'alex': 2,  # Index for 'alex'
        'reese': 3,  # Index for 'reese'
        'random': 4,  # Index for 'random'
    }

    # Get the garden number for the user
    garden_number = garden_mapping.get(user_name, None)

    if garden_number is None:
        return json.dumps({"error": "User not found"})

    # Load the plant data
    plants_data = load_cultivars()

    if plants_data is None:
        return json.dumps({"error": "Error loading plant data"})

    # Check if the garden number is valid
    if garden_number >= len(plants_data):
        return json.dumps({"error": "Invalid garden number"})

    # Return the garden data for the user
    return json.dumps(plants_data[garden_number])

def get_user_garden(user_name):
    # Map usernames to their respective garden numbers
    garden_mapping = {
        'new': 'garden1.json',  # new -> garden1.json
        'morgan': 'garden2.json',  # morgan -> garden2.json
        'alex': 'garden3.json',  # alex -> garden3.json
        'reese': 'garden4.json',  # reese -> garden4.json
        'random': 'garden5.json',  # random -> garden5.json
    }

    # Get the garden number for the user
    garden_number = garden_mapping.get(user_name, None)

    if garden_number is None:
        return json.dumps({"error": "User not found"})

    # Load the plant data
    plants_data = load_cultivars()

    if plants_data is None:
        return json.dumps({"error": "Error loading plant data"})

    # Check if the garden number is valid
    if garden_number >= len(plants_data):
        return json.dumps({"error": "Invalid garden number"})

    # Return the garden data for the user
    return plants_data[garden_number]

def giveMessage(json_vector):
    # Parse user vector
    try:
        user_vector = json_vector
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return json.dumps({"error": "Invalid JSON input"})

    # Extract user name
    user_name = user_vector.get("user", None)

    if user_name is None:
        return json.dumps({"error": "User name not provided"})

    # Get the user's garden data
    garden_data = get_user_garden(user_name)

    if isinstance(garden_data, str):  # If it's an error message
        return garden_data

    # Extract time scores
    morning_score = user_vector.get("morning", 0)
    evening_score = user_vector.get("evening", 0)
    afternoon_score = user_vector.get("afternoon", 0)

    # Determine the time with the highest score
    time_scores = {
        "morning": morning_score,
        "afternoon": afternoon_score,
        "evening": evening_score,
    }
    max_time = max(time_scores, key=time_scores.get)
    max_score = time_scores[max_time]

    # Assign a message based on the time with the highest score
    messages = {
        "morning": "You're a morning person! Your garden looks best in the early hours.",
        "afternoon": "You love the afternoon sun! Your garden shines brightly during the day.",
        "evening": "Evenings are your favorite time! Your garden is perfect for dusk.",
    }
    time_message = messages.get(max_time, "No specific time preference detected.")

    # Combine results
    combined_result = {
        "message": time_message,
        "garden": garden_data,  # Include the user's garden data
    }

    # Return as JSON string
    #return json.dumps(combined_result)



# Test block
if __name__ == "__main__":
    # Example user vector for testing
    user_vector = {
        "user": "new",
        "morning": 0.8,
        "afternoon": 0.5,
        "evening": 0.3
    }

    # Call the function you want to test
    result = giveMessage(user_vector)
    print("Test Result:", result)