from flask import render_template, make_response
from flask_restful import Resource


class Login(Resource):
   def get(self):
       headers = {'Content-Type': 'text/html'}
       
       return make_response(
           render_template('base.html'), 
           200, headers
           )