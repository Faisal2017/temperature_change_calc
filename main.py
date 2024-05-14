# TODO - refactor vars to config file?

# from flight_temp_pipeline/dataframe_processing import read_csv_and_process
import os
import time
import json

from dataframe_processing import read_csv_and_process

from sql_commands import create_db_table, get_results, get_result_by_id, insert_result

import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# Define the path for uploaded files (ensure this directory exists or create it)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/results', methods=['GET'])
def api_get_results():
    return jsonify(())

@app.route('/api/results/<result_id>', methods=['GET'])
def api_get_result(result_id):
    return jsonify(get_result_by_id(result_id))

@app.route('/api/results/add',  methods = ['POST'])
def api_add_results():
    result = request.get_json()
    return jsonify(insert_result(result))

# @app.route('/api/results/update',  methods = ['PUT'])
# def api_update_user():
#     result = request.get_json()
#     return jsonify(update_result(user))
#
# @app.route('/api/users/delete/<user_id>',  methods = ['DELETE'])
# def api_delete_user(user_id):
#     return jsonify(delete_user(user_id))

@app.route('/csv_file_upload', methods=['POST'])
def upload_csv():
    print('request : ', request.files)

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.endswith('.csv'):
        time_string = time.strftime("%Y%m%d-%H%M%S")
        print('time_string : ', time_string)

        os.makedirs(f'uploads/{time_string}')

        # save file locally
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], time_string, filename)
        file.save(file_path)

        df = pd.read_csv(file_path)

        # time string used to create folder structure
        read_csv_and_process(df, time_string)

        # submit to sqlite
        try:
            r = requests.post('http://127.0.0.1:5000/api/results/add', json={'time_submitted': time_string})

            result_id = json.loads(r.text)
        except:
            print('An exception occurred when sending request to SQLite')

        return jsonify({
            "message": "File successfully uploaded and processed",
            "result_location": f'uploads/{time_string}',
            **result_id
        }), 200

    else:
        return jsonify({"error": "Unsupported file type"}), 400


if __name__ == '__main__':
    create_db_table()
    app.run(debug=True)
