# Standard library imports
import os
import time
import stat
from datetime import datetime

# Third party imports
from flask import send_file

# Local application imports
from .config import NN_UTILS_PATH
from .ProviderInterface import ProviderInterface

class FrameDifferenceProvider(ProviderInterface):
    file_path = f'{NN_UTILS_PATH}/frame_difference.py'
    base_route = f'{ProviderInterface.base_route}/framedifference'
    
    def get(self):
        file_status = os.stat(FrameDifferenceProvider.file_path)
        last_modified = time.ctime(file_status[stat.ST_MTIME])
        last_modified = datetime.strptime(last_modified,"%a %b %d %H:%M:%S %Y")
        
        return send_file(FrameDifferenceProvider.file_path, 
                         as_attachment = True,
                         download_name=f'Frame Difference.{last_modified}.py')        