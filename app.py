from flask import Flask, render_template, request
from AutomicLogin import *
import json
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/post', methods=["POST"])
def post():
    username = request.form['username']
    password = request.form['password']
    user = AutomicLogin(username, password)
    return json.dumps({'message': user.testLogin()})
    
if __name__ == '__main__':
    app.run(debug=True)