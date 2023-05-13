import os
import time
import stat
from datetime import datetime

from flask_restful import Resource
from flask import send_file

from . import NN_UTILS_PATH

class FrameDifferenceProvider(Resource):
    file_path = f'{NN_UTILS_PATH}/frame_difference.py'
    request_endpoint = 'framedifference'
    
    def get(self):
        
        file_status = os.stat(FrameDifferenceProvider.file_path)
        last_modified = time.ctime(file_status[stat.ST_MTIME])
        last_modified = datetime.strptime(last_modified,"%a %b %d %H:%M:%S %Y")
        
        return send_file(FrameDifferenceProvider.file_path, 
                         as_attachment = True,
                         download_name=f'Frame Difference.{last_modified}.py')        