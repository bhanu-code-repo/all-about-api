# importing required packages
from flask import Flask, request, jsonify
import mysql.connector as conn

# create flask app
app = Flask(__name__)


@app.route('/get-data', methods=['POST'])
def get_data():
    # get request body
    request_body = request.json

    # create cursor
    if 'username' in request_body.keys() and 'password' in request_body.keys():
        my_db = conn.connect(host='localhost', user=str(request_body['username']),
                             passwd=str(request_body['password']))
        cursor = my_db.cursor()

        # get data from database
        if 'query' in request_body.keys():
            cursor.execute(request_body['query'])
            return jsonify({'data': str(cursor.fetchall())})
    return jsonify({'error': 'username or password not found'})


# run flask app
if __name__ == '__main__':
    app.run(host='localhost', port=9001, debug=True)
