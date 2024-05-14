# TODO - refactor vars to config file?

# from flight_temp_pipeline/dataframe_processing import read_csv_and_process

from dataframe_processing import read_csv_and_process

from sql_commands import create_db_table, get_results, get_result_by_id, insert_result

from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os
from flask import Flask, request, jsonify
from flask_cors import CORS


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
    print('result : ', result)
    return jsonify(insert_result(result))

# @app.route('/api/results/update',  methods = ['PUT'])
# def api_update_user():
#     result = request.get_json()
#     return jsonify(update_result(user))
#
# @app.route('/api/users/delete/<user_id>',  methods = ['DELETE'])
# def api_delete_user(user_id):
#     return jsonify(delete_user(user_id))

@app.route("/summary")
def summary():
    d = {0: 'return data'}
    return d


@app.route('/csv_file_upload', methods=['POST'])
def upload_csv():
    print('request : ', request.files)

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.endswith('.csv'):
        # save file locally
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        df = pd.read_csv(file_path)

        read_csv_and_process(df)

        return jsonify({"message": "File successfully uploaded and processed", "filename": filename}), 200

    else:
        return jsonify({"error": "Unsupported file type"}), 400


if __name__ == '__main__':
    create_db_table()
    app.run(debug=True)

# if __name__ == "__main__":
#     #app.debug = True
#     #app.run(debug=True)
#     app.run() #run app