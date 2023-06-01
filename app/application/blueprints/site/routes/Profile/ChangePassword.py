# Third party imports
from flask import render_template, make_response, flash, redirect
from flask_login import login_required, current_user

from app.application.controllers.cache import cache
from .ProfileInterface import ProfileInterface
from ...forms import ChangePasswordForm
from .....database import db
from .....database.models import User

class ChangePassword(ProfileInterface):
    base_route = f'{ProfileInterface.base_route}/change-password'
    
    @login_required
    @cache.cached(timeout = None)
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        change_password_form = ChangePasswordForm()
        
        return make_response(
            render_template('change-password.html',
                            form = change_password_form), 
            200, headers
        )
        
    @login_required
    def post(self):
        headers = {'Content-Type': 'text/html'}
        
        change_password_form = ChangePasswordForm()
        
        if change_password_form.validate_on_submit():            
            user = User.query.filter_by(id = current_user.id).first()
            
            old_pwd = change_password_form.old_password.data
            new_pwd = change_password_form.new_password.data
            repeat_new_pwd = change_password_form.repeat_password.data
            
            if not user.check_password(old_pwd):
                flash('Parola veche nu este corectă!', 'error')
                return redirect("/profile/change-password")
            
            if new_pwd != repeat_new_pwd:
                flash('Cele două parole nu coincid!', 'error')
                return redirect("/profile/change-password")
            
            if user.check_password(new_pwd):
                flash('Parola nouă nu poate fi identică cu cea veche!', 'error')
                return redirect("/profile/change-password")
            
            user.set_password(new_pwd)
            db.session.add(user)
            db.session.commit()
            
            flash('Parola a fost modificată cu succes!')
            return redirect('/profile/change-password')
                
        return make_response(
            render_template('change-password.html',
                            form = change_password_form), 
            200, headers
        )