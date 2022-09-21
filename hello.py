from flask import Flask,redirect, url_for, render_template, request,session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = {"xyz": generate_password_hash("xyz")}
user = {"username": "abc", "password": "abc"}
user2 = {"username": "admin", "password": "admin"}



@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
     return username



@app.route('/')
@auth.login_required
def index():
    return redirect(url_for('login'))
    

@app.route('/login',methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect(url_for('dashboard'))
            
 
    return render_template('login.html')

@app.route('/users/dashboard')
def dashboard():
    json_uri = requests.get("https://dummyjson.com/products?limit=5")
    posts = (json_uri.json())['products']
    if('user' in session and session['user'] == user['username']):
         
        return render_template("dashboard.html", user=user,  posts = posts)
    else:
        return redirect(url_for('login'))
    
    
    
     
@app.route("/post/<id>", methods=['GET', 'POST'])
def post(id):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')       
        json_uri = requests.get("https://dummyjson.com/products?limit=5")
        
        id = int(id)-1
        
        post = (json_uri.json())['products'][id]
        
        if username == user2['username'] and password == user2['password']:
          session['user2'] = username
          print(post)
          return render_template("details_post.html", user2=user2, post = post)
    else:
     return redirect(url_for('login'))
     
 


@app.route("/users/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)