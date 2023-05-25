# Third party imports
from flask import render_template, make_response, redirect, flash, request
from flask_login import current_user, login_user
from werkzeug.urls import url_parse


# Local application imports
from .ViewerInterface import ViewerInterface
from ..forms import LoginForm
from ....database.models import User

class Login(ViewerInterface):
    base_route = f'{ViewerInterface.base_route}/login'
    
    def get(self):
        if current_user.is_authenticated:
            return redirect('/')
        
        headers = {'Content-Type': 'text/html'}
       
        login_form = LoginForm()
        return make_response(
            render_template('login.html', form=login_form), 
            200, headers
            )
        
    def post(self):
        headers = {'Content-Type': 'text/html'}
        
        login_form = LoginForm()
        
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            
            if user is None or not user.check_password(login_form.password.data):
                flash('Adresa de email sau parola introduse sunt greșite!', 'login_fail')
                return redirect('/login')
        
            login_user(user, remember = True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = '/'
            return redirect(next_page)
                
        return make_response(
            render_template('login.html', form=login_form), 
            200, headers
        )