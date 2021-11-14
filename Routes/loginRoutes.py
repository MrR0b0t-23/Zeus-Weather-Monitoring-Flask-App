from flask import Blueprint, render_template, request,  redirect, url_for, make_response
from database import db

login = Blueprint("login", __name__ ,  template_folder='Templates', static_folder= 'static')

class userData(db.Model):
    __tablename__ = 'User_Database'

    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    def __init__ (self, UserId, Username, Password):
        self.UserId= UserId
        self.Username= Username
        self.Password = Password

def auth_login(username, password):
   token = userData.query.filter(userData.Username.like(username)).filter(userData.Password.like(password)).first()
   if token:
      return True
   return False

@login.route('/', methods =[ 'POST', 'GET'])
def login_page():
    if request.method == 'POST':
       # getting input with name = fname in HTML form
       username = request.form.get("username")
       password = request.form.get("password")
       resp = make_response(redirect(url_for('maps.map_page')))
       if auth_login(username, password):
          resp.set_cookie('Authentication', 'True')
          return resp 
       resp.set_cookie('Authentication', 'False') 
       return render_template('LoginPageHTML.html')

    return render_template('LoginPageHTML.html')
   