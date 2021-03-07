from flask import Flask, render_template, request
from face_r import recognize
from db_query import recipe, get_drinks

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/face')
def face():
    name = recognize(1).capitalize()
    return render_template('index.html', name=name)

@app.route('/recipe', methods=['GET','POST'])
def recipe():
    drinks = get_drinks()
    drink = request.form.get('drink')
    drink_recipe = recipe(drink)
    drink_select = drink
    return render_template('drink.html', drink_recipe=drink_recipe, drinks=drinks, drink_select=drink_select)
