import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
log_file = os.path.join(BASE_DIR, 'app.log')
log_js = os.path.join(BASE_DIR, 'app.js')

def write_log(status, log_message):
    """

    :type status: String
    :type log_message: String
    """
    with open(log_file, 'a') as log:
        timestamp = datetime.now()
        log.write(f'{timestamp},{status},{log_message}\n')


def read_log():
    log_data = []
    with open(log_file, "r") as file:
        data = file.readlines()
        with open(log_js, 'w') as js_file:
            f'new gridjs.Grid(  columns: ["Timestamp", "Log_code", "Log_Message"], search: true, data: ['

            for line in data[1:]:
                log_data.append([line.strip()[0:26], line.strip()[27:28], line.strip()[29:]])
        # print(log_data)
        # return log_data
        # # return data

