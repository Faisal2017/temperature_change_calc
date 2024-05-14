# TODO - refactor vars to config file?

# from flight_temp_pipeline/dataframe_processing import read_csv_and_process

from dataframe_processing import read_csv_and_process

from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Define the path for uploaded files (ensure this directory exists or create it)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

        # Here you could add processing logic, e.g., reading the file with pandas
        df = pd.read_csv(file_path)
        # Process data as required
        # print(df.head())  # Example process: print the first few lines

        read_csv_and_process(df)

        return jsonify({"message": "File successfully uploaded and processed", "filename": filename}), 200

    else:
        return jsonify({"error": "Unsupported file type"}), 400


if __name__ == '__main__':
    app.run(debug=True)
