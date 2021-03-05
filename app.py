from flask import Flask, render_template
from face_r import recognize

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/face')
def face():
    name = recognize(1).capitalize()
    return render_template('index.html', name=name)
