from flask import Flask, render_template, request
from face_r import recognize
from db_query import get_all_drinks, get_availble_recipe
from motor_control import test_pump

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/face')
def face():
    name = recognize(1).capitalize()
    return render_template('index.html', name=name)

@app.route('/recipes', methods=['GET','POST'])
def recipes():
    drinks = get_all_drinks()
    drink = request.form.get('drink')
    drink_recipe = get_availble_recipe(drink)
    drink_select = drink
    return render_template('drink.html', drink_recipe=drink_recipe, drinks=drinks, drink_select=drink_select)

@app.route('/run_pump')
def run_pump():
    test_pump()
    return 'Kek'
