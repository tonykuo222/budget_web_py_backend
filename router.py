from flask import Flask, request, send_file
from flask_cors import CORS

from os import listdir

from constants import *
from controllers.json_parsers import JSONParsers as JSON
from controllers.data_handlers import DataHandlers as DH

app = Flask(__name__)
CORS(app)

# All computation other than non-null checks done through data_handler and json_parsers class
# Calls go to to Data-Handler through json parser class if a json object needs to be returned
#############################################################################################

#default route to check if server is running properly
@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

#Index for all files in resource directory, may be needed by frontend in future
@app.route('/data', methods=['GET'])
def data_index():
    html = get_filenames()
    return html

#Getter for bundled data, packages data => json and formatted line data => json into two keys, "data" and "line_data"
@app.route('/data/<filename>', methods=["GET"])
def data(filename):
    return JSON.fetch_data(filename)

#saves file to proper directory loads in data, updates data.p and returns json
#inserts to data.p and returns success or failure
@app.route('/data', methods=["POST"])
def post_data():
    file = request.files['file']
    card_type = request.args['cardType']
    if(file):
        DH.save_and_insert_file(file, card_type)
        return "Success"
    return "Failed"

@app.route('/initialize_table', methods=["POST"])
def initialize_table():
    file = request.files['file']
    return JSON.initialize_table(file)

# Updates cell with new value and sends back 'status' JSON
@app.route('/update_cell', methods=["PATCH"])
def update_cell():
    return JSON.patch_data(request.json)
    
# Adds a new entry to the table in proper order, re-adjusts calculated values
# returns 'status' JSON
@app.route('/new_entry', methods=["PATCH"])
def new_entry():
    return JSON.patch_new_entry(request.json)

@app.route('/delete_entry', methods=["DELETE"])
def delete_entry():
    return JSON.delete_entry(request.json)

# Saves current data as backup, filetype is dependent on submitted filename
# returns 'status' JSON
@app.route('/save_backup', methods=["POST"])
def save_backup():
    return JSON.save_backup(request.json)

# Loads in current data as given filetype, sends up to frontend
@app.route('/export_file', methods=["POST"])
def export_file():
    address = DH.export_file(request.json)
    try:
        return send_file(address)
    except Exception as e:
        return str(e)

# resets data.p based on submitted filename
@app.route('/reset', methods=["PATCH"])
def reset_pickle():
    return JSON.reset_from_backup(request.json)

##############################################################################
#helper funciton for /data index route
def get_filenames():
    html = "<ul>"
    for filename in listdir('resources'):
        html += "<li>" + filename + "</li>"
        if(filename == "csv"):
            html += "<ul>"
            for filename in listdir('resources/csv'):
                html += "<li>" + filename + "</li>"
            html += "</ul>"
        if(filename == "xl"):
            html += "<ul>"
            for filename in listdir('resources/xl'):
                html += "<li>" + filename + "</li>"
            html += "</ul>"
        if(filename == "pickle"):
            html += "<ul>"
            for filename in listdir('resources/pickle'):
                html += "<li>" + filename + "</li>"
            html += "</ul>"
    html += "</ul>"
    return html