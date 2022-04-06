# importing required packages
import time, requests
from benedict import benedict

# define config file path
config_file_path = 'service_config.ini'

# define service monitoring flag
service_monitor_flag = True


# update service running status
def update_config(service, value=False):
    config_file = benedict.from_ini(config_file_path)
    config_file[service]['status'] = value
    config_file.to_ini(filepath=config_file_path)


# function to check service heartbeats
def check_services(config_data):
    for service, value in config_data.items():
        if service != 'service-monitor':
            url = f'http://localhost:{str(value["port"])}/api/v1/check-service?signal=ping'
            try:
                requests.get(url=url)
            except requests.exceptions.RequestException as error:
                update_config(service)
                print(f'{service} is down, port number {value["port"]}')


# monitor services
while service_monitor_flag:
    print('service monitoring is on ...')
    app_config = benedict.from_ini(config_file_path)
    if not app_config['service-monitor']['state']:
        break
    sleep_time = int(app_config['service-monitor']['time'])
    check_services(app_config)
    time.sleep(sleep_time)
