# importing required packages
from flask import Flask, request
from benedict import benedict

# define config file path
config_file_path = 'service_config.ini'

# define service name
service_name = 'service-four'


# get service configurations
def get_config():
    config_file = benedict.from_ini(config_file_path)
    return int(config_file[service_name]['port']), bool(config_file[service_name]['debug'])


# create flask application
app = Flask(__name__)


# create service monitoring route
@app.route('/api/v1/check-service', methods=['GET'])
def heartbeat():
    signal = request.args.to_dict()['signal']
    return 'pong' if signal == 'ping' else 'invalid-request'


# run flask application
if __name__ == '__main__':
    port_number, debug_flag = get_config()
    app.run(host='localhost', port=port_number, debug=debug_flag)