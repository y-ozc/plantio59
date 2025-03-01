from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os


app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all origins


DATA_FILES = {
    "new": os.path.join("data", "garden1.json"),
    "morgan": os.path.join("data", "garden2.json"),
    "alex": os.path.join("data", "garden3.json"),
    "reese": os.path.join("data", "garden4.json"),
}

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
    with open(os.path.join("data", "cultivars_data.json"), 'r') as file:
        return json.load(file)

# Write to JSON file
def write_json(data, dataset):
    file_path = DATA_FILES.get(dataset, None)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route("/dashboard")
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'dashboard.html')

@app.route("/reccomend")
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'recPage.html')

@app.route("/task")
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taskPage.html')



# API Route: Get all data
@app.route("/api/data", methods=["GET"])
def get_data():
    dataset = request.args.get("dataset", "new")  # Default to "new"
    data = read_json(dataset)  # Pass dataset name to read_json
    return jsonify(data)


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

        write_json(data, dataset)

        return jsonify({"message": "Item added successfully!"}), 201
    else:
        return jsonify({"error": "Invalid item type selected"}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigns a PORT dynamically
    app.run(debug=False, host="0.0.0.0", port=port)
