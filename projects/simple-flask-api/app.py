# importing required packages
from flask import Flask, request, jsonify

# create app - object of Flask class
# note: "app" name can be anything you like, it's just object name i.e. bhanu = Flask(__name__)
app = Flask(__name__)


# create home route with GET method
@app.route('/', methods=['GET'])
def home():
    return 'hello, welcome to flask app'


# run flask app
app.run(host='localhost', port=9000, debug=True)