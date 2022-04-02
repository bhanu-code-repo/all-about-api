# importing required packages
from flask import Flask, request, jsonify

# create app - object of Flask class
app = Flask(__name__)


# create home route with GET method
@app.route('/', methods=['GET'])
def home():
    return 'hello, welcome to flask app'


# create route with POST method
# request url: http://localhost:9000/add
# set request type: POST
# set request header Content-Type as application/json
# request body: {"num1": 25, "num2": 25}
@app.route('/add', methods=['POST'])
def add():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        body = request.json
        return jsonify({'result': body['num1'] + body['num2']})
    else:
        return 'Content-Type not supported!'


# helper function to perform computation
def perform_computation(val1, val2, operation):
    if operation == 'add':
        return val1 + val2

    if operation == 'subtract':
        return val1 - val2

    if operation == 'divide':
        return val1 / val2

    if operation == 'multiply':
        return val1 * val2


# create route with GET, POST method
# ********************************************************
# for using GET
# request url: http://localhost:9000/compute
# set request type: GET
# ********************************************************
# request url: http://localhost:9000/compute
# set request type: POST
# set request header Content-Type as application/json
# request body: {"num1": 5, "num2": 5, "operation": "multiply"}
# note: "operation" values can be one out of add, subtract, divide, multiply
# ********************************************************
@app.route('/compute', methods=['GET', 'POST'])
def compute():
    # handle all GET requests
    if request.method == 'GET':
        return jsonify('supported operations: add, subtract, divide, multiply')

    # handle all POST requests
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.json
            return jsonify({'result': perform_computation(body['num1'], body['num2'], body['operation'])})
        else:
            return 'Content-Type not supported!'


# run flask app - by default flask will run on port number 5000
if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)
