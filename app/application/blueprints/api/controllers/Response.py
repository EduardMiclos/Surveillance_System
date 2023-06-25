from flask import jsonify
from datetime import datetime

class Response:
    def __init__(self):
        self.json = {}
        
    def get_code(self):
        return self.json['Code']

    def set_code(self, code):
        self.json['Code'] = code

        
    def get_status(self):
        return self.json['Status']
    
    def set_status(self, status):
        self.json['Status'] = status

         
    def get_message(self):
        return self.json['Message']
    
    def set_message(self, message):
        self.json['Message'] = message
    
        
    def add_data(self, key, value):
        if 'Data' not in self.json:
            self.json['Data'] = {}
            
        self.json['Data'][key] = value
        
    def get_data(self):
        return self.json['Data']
    
    def get_response(self):
        self.json['Date'] = datetime.now()
        return jsonify(self.json)
    
    def set_success(self):
        self.set_code(200)
        self.set_message('Success')
        
    def set_not_found(self):
        self.set_code(404)
        self.set_status("Not found")
        
    def set_forbidden(self):
        self.set_code(403)
        self.set_status("Access denied!")
        