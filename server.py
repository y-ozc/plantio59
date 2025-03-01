from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins


DATA_FILES = {
    "new": "garden1.json",
    "morgan": "garden2.json",    
    "alex": "garden3.json",
    "reese": "garden4.json"
}

DATA_FILE = "garden2.json"  # JSON file to store data

# Read JSON file
def read_json(dataset):
    file_path = DATA_FILES.get(dataset, None)

    if file_path:  
        try:
            with open(file_path, "r") as f:
                return json.load(f)  # Load the JSON file
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found
            
    else:
        return []  # Return an empty list if dataset is invalid
    
# Function to load item types from the external JSON file
def load_item_types():
    with open('cultivars_data.json', 'r') as file:
        return json.load(file)

# Write to JSON file
def write_json(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# API Route: Get all data
@app.route("/api/data", methods=["GET"])
def get_data():
    dataset = request.args.get("dataset", "new")  # Default to "new"
    data = read_json(dataset)  # Pass dataset name to read_json
    return jsonify(data)

# # API Route: Add new entry
# @app.route("/api/data", methods=["POST"])
# def add_data():
#     new_entry = request.json
#     data = read_json()
#     data.append(new_entry)
#     write_json(data)
#     return jsonify({"message": "Data added successfully!"}), 201


# Route to add new data (POST request for user to submit a new item)
@app.route('/api/data', methods=['POST'])
def add_data():
    dataset = request.args.get("dataset", "new")  # Default to "new"

    # Parse the incoming JSON request data
    new_item = request.get_json()
    print("Received data:", new_item)  
   
    # Get the item type index from the request
    type_index = int(new_item.get("type_index", -1))
    print("Selected type_index:", type_index)


    item_types = load_item_types()  # Load item types from the JSON file

    if type_index >= 0 and type_index < len(item_types):
        selected_item_type = item_types[type_index]  # Fetch the selected item type

        # Combine the new item with the properties of the selected item type
        new_item_data = {
            "name": new_item.get("name"),
            "cultivar": selected_item_type["cultivarName"],
            "eoc": selected_item_type["EOC"],
            "lastLogSince": "0"
        }

        # Load existing data from garden2.json
        data = read_json(dataset)


        # Add the new item to the main data collection
        data.append(new_item_data)

        write_json(data)

        return jsonify({"message": "Item added successfully!"}), 201
    else:
        return jsonify({"error": "Invalid item type selected"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
