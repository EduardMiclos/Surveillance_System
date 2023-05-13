import os
import time
import stat
from datetime import datetime

from flask_restful import Resource
from flask import send_file

from . import NN_UTILS_PATH

class CenterCropProvider(Resource):
    file_path = f'{NN_UTILS_PATH}/center_crop.py'
    request_endpoint = 'centercrop'
    
    def get(self):
        
        file_status = os.stat(CenterCropProvider.file_path)
        last_modified = time.ctime(file_status[stat.ST_MTIME])
        last_modified = datetime.strptime(last_modified,"%a %b %d %H:%M:%S %Y")
        
        return send_file(CenterCropProvider.file_path, 
                         as_attachment = True,
                         download_name=f'Center Crop.{last_modified}.py')        