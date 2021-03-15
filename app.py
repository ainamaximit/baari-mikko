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
    TODO: Improve security.
    """
    def __init__(self, username):
        self.id = username


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
    Login is done by @login_required decorator
    TODO: Review this quick implementation and improve safety if needed
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
        print(name)
        login_user(user)
        return redirect(next_page)
    else:
        return redirect(url_for('index'))


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    """
    This is homepage.
    :return: Index view
    """
    if current_user.is_authenticated:
        name = current_user.id
    else:
        name = None
    return render_template('index.html', name=name)


@app.route("/logout")
@login_required
def logout():
    """
    Logs user out.
    :return: Redirect index view.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/live_feed')
def live_feed():
    """
    Img stream for camera device.
    :return: img stream
    """
    # Return camera frames as jpg
    return Response(feed(video_camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/drinks')
@login_required
def drinks():
    """
    Presents all available drinks.
    :return: Drinks view.
    """
    name = current_user.id
    result = dbi.read_query(Dbq.AVAILABLE_DRINKS)
    all_drinks = [item for t in result for item in t]
    return render_template('drinks.html', name=name, drinks=all_drinks)


@app.route('/mix_drink', methods=['GET', 'POST'])
@login_required
def mix_drink():
    """
    TODO: Makes drink activating pump_controller.py
    :return: JSON recipe of drink from post
    """
    drink = request.form.get('drink')
    drink_recipe = json.dumps(dbi.read_query(Dbq.AVAILABLE_RECIPE, drink))
    return drink_recipe


@app.route('/admin')
@login_required
def admin():
    """
    TODO: Admin validation
    :return: Admin view
    """
    name = current_user.id
    if current_user.id in ("Niko Rintamäki", 'root'):
        return render_template('admin.html', name=name)
    else:
        return redirect(url_for('index'))


@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    """
    TODO: comment
    :return:
    """
    if current_user.id in ("Niko Rintamäki", 'root'):
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
    TODO: comment
    :return:
    """
    if request.method == 'POST':
        usertodel = request.form.get('usertodel')
        response = dbi.execute_query(Dbq.DELETE_USER, (usertodel,))
        print(response)
    # username from POST
    all_users = dbi.read_query(Dbq.USERS)
    return render_template('delete.html', all_users=all_users)


@app.route('/register')
@login_required
def register():
    """
    TODO: comment
    :return:
    """
    name = current_user.id
    if current_user.id in ("Niko Rintamäki", 'root'):
        return render_template('register.html', name=name)
    else:
        return redirect(url_for('index'))


@app.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    """
    TODO: Edit recipes functionality
    :return:
    """
    name = current_user.id
    if current_user.id in ("Niko Rintamäki", 'root'):
        all_drinks = dbi.read_query(Dbq.ALL_DRINKS)
        ingredients = dbi.read_query(Dbq.ALL_INGREDIENTS)
        drink_select = request.form.get('drink')
        drink_recipe = dbi.read_query(Dbq.RECIPE, drink_select)
        return render_template('recipes.html', name=name, drink_select=drink_select, drinks=all_drinks,
                               drink_recipe=drink_recipe, ingredients=ingredients)
    else:
        return redirect(url_for('index'))
