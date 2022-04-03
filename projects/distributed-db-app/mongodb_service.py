# importing required packages
import pymongo
from flask import Flask, request, jsonify

# create flask app
app = Flask(__name__)


@app.route('/get-data', methods=['POST'])
def get_data():
    # get request body
    request_body = request.json

    # create mongodb client
    if 'connection-string' in request_body.keys():
        client = pymongo.MongoClient(str(request_body['connection-string']))
        db = client.BPST
        collection = db['my_collection']
        return jsonify({'data': str(list(collection.find()))})
    return jsonify({'error': 'connection-string not found'})


# run flask app
if __name__ == '__main__':
    app.run(host='localhost', port=9002, debug=True)
