from flask import Flask, render_template, request, Response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from facecam import compare, capture, learn, feed, VideoCamera
from databaseinterface import DatabaseInterface
from databasequeries import DatabaseQueries as Dbq
import json

dbi = DatabaseInterface("test1", "mikko", "baari", "127.0.0.1")

app = Flask(__name__, static_url_path='/static')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.secret_key = 'penis'


global video_camera
video_camera = None

if video_camera is None:
    video_camera = VideoCamera()


class User(UserMixin):
    """
    User class for login. Has all necessary features provided by UserMixin class.
    Our app only uses name for auth.
    """

    def __init__(self, username):
        self.id = username
        self.admin = False
        result = dbi.read_query(Dbq.USER_IS_ADMIN, (username,))
        if result:
            if result[0][0]:
                self.admin = result[0][0]

    @staticmethod
    def is_admin(self):
        return self.admin


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    """
    This is homepage.
    :return: Index view
    """

    if current_user.is_authenticated:
        logged = current_user.is_authenticated
        admin = current_user.is_admin
        name = current_user.id
    else:
        logged = False
        admin = False
        name = None

    return render_template('index.html', logged=logged, name=name, admin=admin)


@login_manager.user_loader
def load_user(name):
    """
    Loader for users. Flask-Login depends this.
    :param name: User string (name)
    :return: User object from user class
    """
    user = User(name)

    return user


@app.route('/login')
def login():
    """
    Logs user in if face recognition matches the user database.
    Login is verified by @login_required decorator
    :return: Redirect to protected page that was requested if login valid.
    """
    # get list of users
    result = dbi.read_query(Dbq.USERS_NAMES)
    users = [i[0] for i in result]
    faces = dbi.read_query(Dbq.USERS_FACES)
    name = compare(5, faces)
    if name in users:
        next_page = request.args.get('next')
        user = User(name)
        login_user(user)
        return redirect(next_page)
    else:
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
    return render_template('drinks.html', name=name, drinks=available_drinks)


@app.route('/mix_drink', methods=['GET', 'POST'])
@login_required
def mix_drink():
    """
    TODO: Makes drink by activating pump_controller.py
    :return: JSON recipe of drink from post
    """
    drink = request.form.get('drink')
    drink_recipe = json.dumps(dbi.read_query(Dbq.AVAILABLE_RECIPE, drink))
    return drink_recipe


@app.route('/admin')
@login_required
def admin():
    """
    Administrator view.
    Has links to create user, change recipes, etc.
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
        img_path = capture(username)
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
        usertodel = request.form.get('usertodel')
        dbi.execute_query(Dbq.DELETE_USER, (usertodel,))
    all_users = dbi.read_query(Dbq.USERS)
    return render_template('delete.html', all_users=all_users)


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


@app.route('/live_feed')
def live_feed():
    """
    Img stream from camera. Use this as img source in html or css.
    :return: image
    """
    # Return camera frames as jpg
    return Response(feed(video_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
