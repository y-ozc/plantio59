import json
import random



cultivars_data = json.loads('data\\cultivars_data.json')

def pick_category(user_vector):

    # Get categories
    selected_items = list(user_vector.items())[1:5]  # Slice from second to fifth entry

    # Unzip keys and values
    _, weights = zip(*selected_items)  # Ignore names, keep weights
    
    # Pick a number from 1 to 4 using weights
    return random.choices(range(1, 5), weights=weights)


def get_categories(category):

    filtered_cultivars = [item for item in cultivars_data if item['category'] == category]
    
    return filtered_cultivars


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
    combined_result = {"alley": alley_pick, "simple": simple_pick, "challenge": challenge_pick}

    # Convert to JSON string for easy transmission to JavaScript
    return json.dumps(combined_result)





