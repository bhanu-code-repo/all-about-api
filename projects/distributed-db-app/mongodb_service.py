# importing required packages
import pymongo
from flask import Flask, request, jsonify

# create flask app
app = Flask(__name__)


# helper function to validate incoming request body
def validate_request_body(required_keys, actual_keys):
    status = True
    for key in required_keys:
        if key not in actual_keys:
            status = False
    return status


@app.route('/get-data', methods=['POST'])
def get_data():
    # get request body
    request_body = request.json

    # create mongodb client
    if validate_request_body(['connection-string', 'db-name', 'collection'], request_body.keys()):
        client = pymongo.MongoClient(str(request_body['connection-string']))
        db = client[request_body['db-name']]
        collection = db[request_body['collection']]
        return jsonify({'data': str(list(collection.find()))})
    return jsonify({'error': 'db-name or collection or connection-string not found'})


# run flask app
if __name__ == '__main__':
    app.run(host='localhost', port=9002, debug=True)
