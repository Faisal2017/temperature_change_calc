Getting Started


Build the Docker image:

`
docker build -t flask-app .
`


Run the Docker image while mounting the container volumne onto a local volume so that the flies produced by the container are also produced locally.

Replace "/home/fal/Desktop/rocketlab/flight_temp_pipeline/uploads" with your local upload path.


`
docker run -p 5000:5000 -v /home/fal/Desktop/rocketlab/flight_temp_pipeline/uploads:/flight_temp_pipeline/uploads flask-app
`

This starts the API on http://localhost:5000.


To submit a CSV to the API, replacing the file location with your own local path :

`
curl -X POST -F "file=@/home/fal/Desktop/rocketlab/FlightAcl.csv" http://localhost:5000/csv_file_upload
`


This will return:

{"message":"File successfully uploaded and processed","result_id":1,"result_location":"uploads/20240515-124215","time_submitted":"20240515-124215"}


Note - the only way to access the files atm is locally, so you should be able to see the files in directory mounted when running the Docker run command.

So in my example this means I can find the output files at "/home/fal/Desktop/rocketlab/flight_temp_pipeline/uploads/20240515-124215"


The API returns a "result_id" which can be queried with:

`
curl http://127.0.0.1:5000/api/results/1
`

To get the "time_submitted" string. This was with the intention of being able to get query results back at a later date using the 'result_id'.

"Users" was something I would've added as well so you can see a list of the users and list of all reports submitted.



To run tests

PYTHONPATH=. pytest

THINGS TO IMPROVE ON:

- add functionality to return the flies through the API
- more tests, especially around the files submitted thru the API
- setting up a local Kubernetes deployment
