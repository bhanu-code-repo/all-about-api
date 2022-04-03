# importing required packages
import requests
from flask import Flask, request, jsonify

# create flask app
app = Flask(__name__)


# helper function to check request body content type
def check_content_type(incoming_request):
    status = False
    content_type = incoming_request.headers.get('Content-Type')
    if content_type == 'application/json':
        status = True
    return status


# make GET request
def make_GET_request(port, service):
    url = 'http://localhost:port/service'.replace('port', port).replace('service', service)
    return requests.get(url)


# make POST request
def make_POST_request(port, service, payload):
    url = 'http://localhost:port/service'.replace('port', port).replace('service', service)
    return requests.post(url=url, json=payload)


# handle incoming request
@app.route('/db-app', methods=['GET', 'POST'])
def handle_app_requests():
    # handle all GET requests
    if request.method == 'GET':
        return jsonify({'supported functions': 'get data', 'supported DB': 'MySQL, MongoDB'})

    # handle all POST requests
    if request.method == 'POST':
        if check_content_type(request):
            request_body = request.json
            if 'type' in request_body.keys():
                if request_body['type'].lower() == 'sql':
                    response = make_POST_request('9001', 'get-data', request_body)
                    return response.json()
                if request_body['type'].lower() == 'mongodb':
                    response = make_POST_request('9002', 'get-data', request_body)
                    return response.json()
        return jsonify({'error': 'Content-Type not supported!'})


# run flask app
if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)
