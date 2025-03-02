import json

BASE_VECTOR = {
    "user": "name",
    "ornament": 0.5,
    "herb": 0.5,
    "crop": 0.5,
    "mushroom": 0.5,
    "eoc_ideal": 0.5,
    "schedule": 1
}

JSON_PATH = 'data\\user_vectors.json'

# STUB
# Takes a garden json and name. 
# Adjusts the base user vector accordingly.
# Saves it to user_vectors.json
def makeUserVector(garden_json, user_name):
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
    makeUserVector('data\\garden1.json')
    makeUserVector('data\\garden2.json')
    makeUserVector('data\\garden3.json')
    makeUserVector('data\\garden4.json')