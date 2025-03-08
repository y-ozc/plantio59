from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import os
import json
from collections import OrderedDict
import recommend
import schedule


app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all origins


# Serve static files from the /data folder
@app.route('/data/<filename>', methods=['GET'])
def get_data(filename):
    try:
        # Define the folder where JSON files are stored
        data_folder = os.path.join(app.root_path, 'data')
        
        # Send the file from the data folder
        return send_from_directory(data_folder, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route("/")
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route("/dashboard.html")
def dash():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'dashboard.html')

@app.route("/recPage.html")
def rec():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'recPage.html')

@app.route("/taskPage.html")
def task():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taskPage.html')

# STUB
@app.route('/api/rec-function', methods=['POST'])
def rec_fn():
    # Get JSON data from the request
    data = request.get_json()
    recommendation = recommend.genRec(data)
    return jsonify({'recommendation': recommendation})

# STUB
@app.route("/api/task-function", methods=['GET'])
def task_fn():
    data = request.get_json()
    message = schedule.giveMessage(data)
    return jsonify({"message": message})



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigns a PORT dynamically
    app.run(debug=True, host="0.0.0.0", port=port)
