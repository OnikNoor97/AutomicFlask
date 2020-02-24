from flask import Flask, render_template, request
from flask_sse import sse
from AutomicLogin import AutomicLogin
import json
import time
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://127.0.0.1"
app.register_blueprint(sse, url_prefix='/post')

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

@app.route('/sse', methods=["POST"])
def sseTest():
    for x in range(0, 3):
        print("We're on time %d" % (x))
        sse.publish({"message": x}, type='publish')
        time.sleep(1)

@route("/stream")
def stream():
    def eventStream():
        while True:
            # Poll data from the database
            # and see if there's a new message
            if len(messages) > len(previous_messages):
                yield "data: "
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)