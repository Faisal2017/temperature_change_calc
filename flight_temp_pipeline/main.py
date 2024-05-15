import os
import sqlite3
import time
import json

from flight_temp_pipeline.dataframe_processing import process_dataframe
from flight_temp_pipeline.sql_commands import create_db_table, get_result_by_id, insert_result

import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# define the path for uploaded files - ensure this directory exists or create it
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def summary():
    d = {0: 'return data'}
    return d


@app.route('/api/results', methods=['GET'])
def api_get_results():
    return jsonify(())


@app.route('/api/results/<result_id>', methods=['GET'])
def api_get_result(result_id):
    return jsonify(get_result_by_id(result_id))


@app.route('/api/results/add', methods=['POST'])
def api_add_results():
    result = request.get_json()
    return jsonify(insert_result(result))


@app.route('/csv_file_upload', methods=['POST'])
def upload_csv():
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
        process_dataframe(df, time_string)

        # submit to sqlite
        try:
            r = requests.post('http://127.0.0.1:5000/api/results/add', json={'time_submitted': time_string})

            result_id = json.loads(r.text)

        except sqlite3.Error as e:
            print(f'An exception occurred when sending request to SQLite: {e}')

        return jsonify({
            "message": "File successfully uploaded and processed",
            "result_location": f'uploads/{time_string}',
            **result_id
        }), 200

    else:
        return jsonify({"error": "Unsupported file type"}), 400


@app.route('/files', methods=['GET'])
def retrieve_files():
    get_timestamp = request.args.get('time_stamp', default='*', type=str)
    print('get_timestamp : ', get_timestamp)


app.run(create_db_table())

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5050)
