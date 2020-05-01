from flask import Flask, request
from flask_cors import CORS

from constants import *
from controllers.json_parsers import JSONParsers as JSON
from controllers.data_handlers import DataHandlers as DH

app = Flask(__name__)
CORS(app)

# All computation other than non-null checks done through data_handler and json_parsers class
# Calls go to to Data-Handler through json parser class if a json object needs to be returned
@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

@app.route('/line_data/<filename>', methods=["GET"])
def line_data(filename):
    cols = None
    if(request.args.get("columns") == "ALL"):
        cols = ColumnSets.BUDGET_ALL
    else:
        cols = ColumnSets.BUDGET_STD
    return JSON.fetch_line_data(filename, cols=cols)

@app.route('/data/<filename>', methods=["GET"])
def data(filename):
    return JSON.fetch_data(filename)

@app.route('/data', methods=["POST"])
def post_data():
    file = request.files['file']
    if(file):
        DH.save_and_print_file(file)
    return "Hello"

@app.route('/print_csv')
def print_csv():
    DH.load_and_print_csv()
    return "Printed"