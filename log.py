import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
log_file = os.path.join(BASE_DIR, 'app.log')


def write_log(status,log_message):
    with open(log_file, 'a') as log:
        timestamp = datetime.now()
        log.write(f'{timestamp},{status},{log_message}')

