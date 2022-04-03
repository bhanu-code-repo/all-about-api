# importing required packages
import json, pymongo


def check_content_type(request):
    status = False
    # get request "Content-Type"
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        status = True
    return status


def read_json_file(filename):
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def write_json_file(filename, data):
    json_object = json.dumps(data, indent=2)
    with open(filename, 'w') as outfile:
        outfile.write(json_object)


def validate_request_body(required_keys, actual_keys):
    status = True
    for key in required_keys:
        if key not in actual_keys:
            status = False
    return status


def process_get_dbs_request(request, cursor, client):
    status = False
    args_dict = {k.lower(): v.lower() for (k, v) in request.args.to_dict().items()}
    if len(args_dict.items()) == 1:
        if 'type' in args_dict.keys():
            if args_dict['type'] == 'sql':
                status = True
                cursor.execute('show databases')
                return status, str([db_name for db_name, in cursor.fetchall()])
            elif args_dict['type'] == 'mongodb':
                try:
                    status = True
                    result = client.list_database_names()
                    return status, result
                except Exception as err:
                    status = False
                    return status, str(err)
            else:
                return status, 'invalid db type'
        else:
            return status, 'db type not specified in url'
    else:
        return status, 'invalid request'


def process_get_db_request(request, cursor):
    status = False
    args_dict = {k.lower(): v.lower() for (k, v) in request.args.to_dict().items()}
    if len(args_dict.items()) == 2:
        if 'db' in args_dict.keys() and 'type' in args_dict.keys():
            if args_dict['type'] == 'sql':
                status = True
                cursor.execute('show databases')
                result = 1 if args_dict["db"] in [str(db_name) for db_name, in cursor.fetchall()] else 0
                return status, f'{args_dict["db"]}#{result}'
            elif args_dict['type'] == 'mongodb':
                status = True
                return status, 'to do'
            else:
                return status, 'invalid db type'
        else:
            return status, 'either db or db type or both not specified in url'
    else:
        return status, 'invalid request'


def process_create_db_request(request, cursor, client):
    status = False
    if check_content_type(request):
        request_body = {k.lower(): v.lower() for (k, v) in request.json.items()}
        if validate_request_body(['name', 'type'], request_body.keys()):
            if request_body['type'] == 'sql':
                status = True
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {request_body["name"]}')
                return status, f'{request_body["name"]} db created successfully'
            elif request_body['type'] == 'mongodb':
                status = True
                db = client[request_body['name']]
                return status, f'{db.name} db created successfully'
            else:
                return status, 'invalid db type'
        else:
            return status, 'request body validation'
    else:
        return status, 'Content-Type not supported!'


# {"name": "fsds_course", "type": "SQL", "query": "SELECT * FROM FSDS_COURSE.STUDENTS"}
def process_get_db_data(request, cursor, collection):
    status = False
    if check_content_type(request):
        request_body = {k.lower(): v.lower() for (k, v) in request.json.items()}
        if validate_request_body(['name', 'type'], request_body.keys()):
            if request_body['type'] == 'sql':
                if validate_request_body(['query'], request_body.keys()):
                    status = True
                    cursor.execute(request_body['query'])
                    return status, cursor.fetchall()
            elif request_body['type'] == 'mongodb':
                status = True
                return status, [data for data in collection.find()]
            else:
                return status, 'invalid db type'
        else:
            return status, 'request body validation'
    else:
        return status, 'Content-Type not supported!'
