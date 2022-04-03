# importing required packages
import os, utils, pymongo
from flask import Flask, request, jsonify
import mysql.connector as conn

# create app - object of Flask class
app = Flask(__name__)


@app.route('/configure-db', methods=['POST'])
def configure_db():
    if utils.check_content_type(request):
        request_body = {k.lower(): v.lower() for (k, v) in request.json.items() if k.lower() != 'conn-str'}
        request_body['conn-str'] = request.json['conn-str']
        if utils.validate_request_body(['username', 'password', 'conn-str'], request_body.keys()):
            utils.write_json_file('config.json', request_body)
            return jsonify({'status': 'db configured successfully'})
        else:
            return jsonify({'error': 'username or password is missing'})
    return jsonify({'error': 'Content-Type not supported!'})


@app.route('/get-dbs', methods=['GET'])
def get_db():
    if 'config.json' in os.listdir('.'):
        app_config = utils.read_json_file('config.json')
        try:
            # create cursor
            my_db = conn.connect(host='localhost', user=str(app_config['username']), passwd=str(app_config['password']))
            cursor = my_db.cursor()

            # create mongodb client
            client = pymongo.MongoClient(app_config['conn-str'])

            # process request
            status, result = utils.process_get_dbs_request(request, cursor, client)
            if status:
                return jsonify({'existing dbs': result})
            else:
                return jsonify({'error': result})
        except conn.Error as err:
            return jsonify({'message': err.msg, 'error code': err.errno, 'sqlstate': err.sqlstate})
    else:
        return jsonify({'error': 'db configuration file not exists'})


@app.route('/check-db', methods=['GET'])
def check_db():
    if 'config.json' in os.listdir('.'):
        app_config = utils.read_json_file('config.json')
        try:
            # create cursor
            my_db = conn.connect(host='localhost', user=str(app_config['username']), passwd=str(app_config['password']))
            cursor = my_db.cursor()

            # process request
            status, result = utils.process_get_db_request(request, cursor)
            if status:
                db_status = 'exists' if int(result.split('#')[1]) == 1 else 'not exists'
                return jsonify({'db name': result.split('#')[0], 'db status': db_status})
            else:
                return jsonify({'error': result})
        except conn.Error as err:
            return jsonify({'message': err.msg, 'error code': err.errno, 'sqlstate': err.sqlstate})
    else:
        return jsonify({'error': 'db configuration file not exists'})


@app.route('/create-db', methods=['GET', 'POST'])
def create_db():
    # handle all GET requests
    if request.method == 'GET':
        return jsonify({'error': 'check request type, it should be POST'})

    # handle all POST requests
    if request.method == 'POST':
        if 'config.json' in os.listdir('.'):
            app_config = utils.read_json_file('config.json')
            try:
                # create cursor
                my_db = conn.connect(host='localhost', user=str(app_config['username']),
                                     passwd=str(app_config['password']))
                cursor = my_db.cursor()

                # create mongodb client
                client = pymongo.MongoClient(str(app_config['conn-str']))

                # process request
                status, result = utils.process_create_db_request(request, cursor, client)
                if status:
                    return jsonify({'db status': result})
                else:
                    return jsonify({'error': result})
            except conn.Error as err:
                return jsonify({'message': err.msg, 'error code': err.errno, 'sqlstate': err.sqlstate})
        else:
            return jsonify({'error': 'db configuration file not exists'})


@app.route('/get-db-data', methods=['GET', 'POST'])
def get_db_data():
    # handle all GET requests
    if request.method == 'GET':
        return jsonify('supported database: SQL, MongoDB')

    # handle all POST requests
    if request.method == 'POST':
        if 'config.json' in os.listdir('.'):
            app_config = utils.read_json_file('config.json')
            try:
                # create cursor
                my_db = conn.connect(host='localhost', user=str(app_config['username']),
                                     passwd=str(app_config['password']))
                cursor = my_db.cursor()

                # create mongodb client
                client = pymongo.MongoClient(str(app_config['conn-str']))
                db = client.BPST
                collection = db['my_collection']

                # process request
                status, result = utils.process_get_db_data(request, cursor, collection)
                if status:
                    return jsonify({'data': str(result)})
                else:
                    return jsonify({'error': result})
            except conn.Error as err:
                return jsonify({'message': err.msg, 'error code': err.errno, 'sqlstate': err.sqlstate})
        else:
            return jsonify({'error': 'db configuration file not exists'})


@app.route('/insert-data', methods=['POST'])
def insert_data():
    if 'config.json' in os.listdir('.'):
        app_config = utils.read_json_file('config.json')
        try:
            # create cursor
            my_db = conn.connect(host='localhost', user=str(app_config['username']),
                                 passwd=str(app_config['password']))
            cursor = my_db.cursor()

            request_body = {k.lower(): v.lower() for (k, v) in request.json.items()}
            if utils.validate_request_body(['name', 'type', 'query'], request_body.keys()):
                if request_body['type'] == 'sql':
                    cursor.execute(request_body['query'])
                    my_db.commit()
                    return jsonify({'status': 'record added successfully'})
        except conn.Error as err:
            return jsonify({'message': err.msg, 'error code': err.errno, 'sqlstate': err.sqlstate})
    else:
        return jsonify({'error': 'db configuration file not exists'})


# run flask app - by default flask will run on port number 5000
if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)
