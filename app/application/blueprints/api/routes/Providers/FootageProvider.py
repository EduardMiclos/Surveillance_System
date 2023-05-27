# Standard library imports
import os
import time
import stat
from datetime import datetime

# Third party imports
from flask import send_file

# Local application imports
from .config import FOOTAGE_PATH
from .FootageProviderInterface import FootageProviderInterface

class FootageProvider(FootageProviderInterface):
    base_route = f'{FootageProviderInterface.base_route}/<string:file_name>'
    
    def get(self, file_name):
        print(FOOTAGE_PATH)
        file_path = f'{FOOTAGE_PATH}/{file_name}'
        return send_file(file_path)        