import json

from flask import Flask, render_template, request, Response, redirect, url_for, send_from_directory
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from facecam import compare, capture, learn, feed, CameraStream
from databaseinterface import DatabaseInterface
from databasequeries import DatabaseQueries as Dbq
from mixer import Mixer
from datetime import datetime
from new_recipe import store_recipe
import multiprocessing as mp
import time
import configparser
import random as rand

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__, static_url_path='/static')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.secret_key = config.get('BAARIMIKKO', 'secret_key')

vs = CameraStream(config.getint('FACECAM', 'camera_source')).start()
dbi = DatabaseInterface(config.get('DATABASE', 'database'),
                        config.get('DATABASE', 'username'),
                        config.get('DATABASE', 'password'),
                        config.get('DATABASE', 'ip_address'))
pool = mp.Pool(mp.cpu_count() - 1)
mixer = Mixer()


class User(UserMixin):
    def __init__(self, username):
        """
        UserMixin class extension for Flask-Login.
        :param username: Users name in database
        """
        self.id = username
        self.img = None
        self.admin = False
        self.serial = None

        user_info = dbi.read_query(Dbq.GET_USER_INFO, (username,))
        print(user_info)
        if user_info:
            if user_info[0][0]:
                self.serial = user_info[0][0]
            if user_info[0][1]:
                self.id = user_info[0][1]
            if user_info[0][2]:
                self.img = user_info[0][2]
            if user_info[0][3]:
                self.admin = user_info[0][3]

    def is_admin(self):
        """
        Tells if current user is admin
        :return: Boolean, is current user admin
        """
        return self.admin

    def get_photo(self):
        return self.img


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    """
    This is homepage.
    :return: Index view
    """

    if current_user.is_authenticated:
        logged = current_user.is_authenticated
        is_admin = current_user.is_admin
        name = current_user.id
    else:
        logged = False
        is_admin = False
        name = None

    return render_template('index.html', logged=logged, name=name, admin=is_admin)


@login_manager.user_loader
def load_user(name):
    """
    Loader for users. Flask-Login depends this.
    :param name: User string (name)
    :return: User object from user class
    """
    return User(name)


@app.route('/login')
def login():
    """
    Logs user in if face recognition matches the user database.
    Login is verified by @login_required decorator
    :return: Redirect to protected page that was requested if login valid.
    """
    # get list of users
    aika = time.time()
    result = dbi.read_query(Dbq.USERS_NAMES)
    users = [i[0] for i in result]
    faces = dbi.read_query(Dbq.USERS_FACES)

    name = compare(vs, pool, faces, config.getint('FACECAM', 'recognize_frames'))
    if name in users:
        next_page = request.args.get('next')
        user_name = User(name)
        login_user(user_name)
        print(f"--- Total login time {time.time() - aika} seconds ---")
        return redirect(next_page)
    else:
        print(time.time() - aika)
        return redirect(url_for('index'))


@app.route("/logout")
@login_required
def logout():
    """
    Logs user out using Flask-Login.
    :return: Redirect index view.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route("/faces/<path:path>")
def faces_dir(path):
    """
    Serves user image folder
    :param path: User img folder
    :return: User img
    """
    return send_from_directory("faces", path)


@app.route('/drinks')
@login_required
def drinks():
    """
    Presents all available drinks.
    :return: Drinks view.
    """
    name = current_user.id
    result = dbi.read_query(Dbq.AVAILABLE_DRINKS)
    available_drinks = [item for t in result for item in t]
    print(available_drinks)
    print(len(available_drinks))

    random = rand.randint(0, len(available_drinks)-1)
    joker = available_drinks[random]
    #available_drinks.append(joker)
    return render_template('drinks.html', name=name, drinks=available_drinks, joker=joker)


@app.route('/history')
@login_required
def history():
    """
    Shows drink history
    :return: History
    """
    name = current_user.id
    user_history = dbi.read_query(Dbq.USER_HISTORY, (current_user.id,))
    # date = user_history[1][3].strftime("%d.%m - %H:%M:%S"))
    return render_template('history.html', name=name, user_history=user_history)


@app.route('/user')
@login_required
def user():
    """
    Shows user info
    :return: User page
    """
    name = current_user.id
    img = current_user.img
    is_admin = current_user.admin
    return render_template('user.html', name=name, img=img, isadmin=is_admin)


@app.route('/mix_drink', methods=['GET', 'POST'])
@login_required
def mix_drink():
    """
    Makes drink by activating mixer.py
    :return: Mixing view
    """
    drink = request.form.get('drink')
    dt = datetime.now()

    print(drink)
    drink_id = dbi.read_query(Dbq.GET_DRINK_ID, (drink,))  # get drink id for order history
    dbi.execute_query(Dbq.ORDER, (current_user.serial, drink_id[0], dt))  # write to order history

    drink_recipe = dbi.read_query(Dbq.AVAILABLE_RECIPE, (drink,))
    print(drink_recipe)
    print(dict(drink_recipe))
    mix_time = 5
    mix_time = mixer.request(dict(drink_recipe))
    return render_template('pumping.html', drink=drink, time=mix_time, drink_recipe=drink_recipe)


@app.route('/admin')
@login_required
def admin():
    """
    Administrator view.
    Has links to register user, delete user and configure pumps.
    :return: Admin view
    """
    name = current_user.id
    if current_user.admin:
        return render_template('admin.html', name=name)
    else:
        return redirect(url_for('index'))


@app.route('/register')
@login_required
def register():
    """
    Register user form
    :return: Register view
    """
    if current_user.admin:
        return render_template('register.html')
    else:
        return redirect(url_for('index'))


@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    """
    Form functionality to add user to database.
    Captures photo of user and saves it to faces.
    Then creates facemapping for facerecognition.
    Finally stores them to database with user name and admin boolean.
    :gets: name, admin from POST
    :return: redirection
    """
    if current_user.admin:
        username = request.form.get('username')
        administrator = request.form.get('admin')
        admin_boolean = False
        if administrator == 'on':
            admin_boolean = True
        img_path = capture(username, vs)
        pickled = learn(username, img_path)
        args = (username, pickled, img_path, admin_boolean)
        dbi.execute_query(Dbq.CREATE_USER, args)
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))


@app.route('/del_user', methods=['POST', 'GET'])
@login_required
def del_user():
    """
    Shows list of users to delete.
    Handles POST to delete user permanently from database.
    TODO: delete stored photo
    :return: delete user view
    """
    if request.method == 'POST':
        user_to_del = request.form.get('usertodel')
        dbi.execute_query(Dbq.DELETE_USER, (user_to_del,))
    all_users = dbi.read_query(Dbq.USERS)
    return render_template('delete.html', all_users=all_users)


@app.route('/prime', methods=['POST', 'GET'])
@login_required
def prime():
    """
    Prime the lines
    :return: delete user view
    """
    prime_qty = config.getint('MIXER', 'priming_quantity')
    if request.method == 'POST':
        qty = int(request.form.get('prime'))
        if qty < 3:
            print("funny")
        else:
            print(f"Priming {qty} ml")
            mixer.prime(qty)
    all_users = dbi.read_query(Dbq.USERS)
    return render_template('prime.html', all_users=all_users, prime_qty=prime_qty)


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    """
    TODO: Edit recipes functionality
    :return:
    """
    name = current_user.id
    if current_user.admin:
        all_drinks = dbi.read_query(Dbq.ALL_DRINKS)
        ingredients = dbi.read_query(Dbq.ALL_INGREDIENTS)
        drink_select = request.form.get('drink')
        drink_recipe = dbi.read_query(Dbq.RECIPE, drink_select)
        return render_template('recipes.html', name=name, drink_select=drink_select, drinks=all_drinks,
                               drink_recipe=drink_recipe, ingredients=ingredients)
    else:
        return redirect(url_for('index'))


@app.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if not current_user.admin:
        return redirect(url_for('index'))

    ingredients = dbi.read_query(Dbq.ALL_INGREDIENTS)
    return render_template('create_recipe.html', ingredients=ingredients)


@app.route('/submit_recipe', methods=['GET'])
@login_required
def submit_recipe():
    if not current_user.admin:
        return redirect(url_for('index'))

    print(request.args)
    args = dict(request.args)
    print(len(args))
    asd = []
    for key, value in args.items():
        print(value)
        asd.append(value)
    name = asd[0]
    qtys = asd[::2]
    qtys.pop(0)
    print(type(qtys))
    # qtysi = [int(i) for i in qtys]
    qtysi = list(map(int, qtys))
    asd.pop(0)
    ings = asd[::2]
    recipe = dict(zip(ings, qtysi))
    print(recipe)
    final = {"name": name, "ingredients": recipe}
    print(json.dumps(final))
    store_recipe(final)


    return redirect(url_for('index'))


@app.route('/pumps', methods=['GET', 'POST'])
@login_required
def pumps():
    if current_user.admin:
        if request.method == 'POST':
            for i in request.form:
                x = request.form.get(i)
                print(f'Set {x} for pump {i}')
                dbi.execute_query(Dbq.SET_PUMP_INGREDIENTS, (i, x))

        at_pumps = dbi.read_query(Dbq.GET_PUMPS_INGREDIENTS)
        ingredients = dbi.read_query(Dbq.ALL_INGREDIENTS)

        return render_template('pumps.html', atpumps=at_pumps, ingredients=ingredients)
    else:
        return redirect(url_for('index'))


@app.route('/live_feed')
def live_feed():
    """
    Img stream from camera. Use this as img source in html or css.
    :return: motion jpeg
    """
    return Response(feed(vs), mimetype='multipart/x-mixed-replace; boundary=frame')
