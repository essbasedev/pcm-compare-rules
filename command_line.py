import os
import uuid
from main import compare_files, write_csv, final_output
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
uploads = os.path.join(BASE_DIR, 'uploads')
output_dir = os.path.join(BASE_DIR, 'downloads')
output_file = os.path.join(output_dir, datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.csv')

file1 = input("Input the path of file #1: \n")
file1_uuid = os.path.join(uploads, uuid.uuid4().hex + ".xml")
os.system(f'cp {file1} {file1_uuid}')
file2 = input("Input the path of file #2: \n")
file2_uuid = os.path.join(uploads, uuid.uuid4().hex + ".xml")
os.system(f'cp {file2} {file2_uuid}')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

compare_files(file1_uuid, file2_uuid)
write_csv(output_file, final_output)