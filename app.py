from flask import Flask, render_template, request, Response, redirect, session, url_for
from facecam import compare, capture, learn, feed, VideoCamera
from databaseinterface import DatabaseInterface
from databasequeries import DatabaseQueries as dbq

dbi = DatabaseInterface("test1", "mikko", "baari", "127.0.0.1")

app = Flask(__name__, static_url_path='/static')
# key for sessions(cookie)
app.secret_key = 'penis'

global video_camera
video_camera = None

if video_camera is None:
    video_camera = VideoCamera()


# Index route at start with two different route names
@app.route('/')
@app.route('/index')
def index():
    # check if user session is set
    name = None
    if 'username' in session:
        # get list of users
        result = dbi.read_query(dbq.USERS_NAMES)
        names = [i[0] for i in result]
        # validate session against registered users
        if session['username'] in names:
            name = session['username']
    if 'admin' in session:
        print('admin')
    return render_template('index.html', name=name)


# Login route with optional redirection.
@app.route('/login/<redirection>')
@app.route('/login')
def login(redirection=None):
    # get list of users
    result = dbi.read_query(dbq.USERS_NAMES)
    names = [i[0] for i in result]
    print(names)
    # check if user session is set
    if 'username' in session:
        # validate session against registered users
        if session['username'] in names:
            if redirection == 'drinks':
                return redirect(url_for('drinks'))
            elif redirection == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('logout'))

    # if there is no session log user in
    else:
        # take x images return most common result
        name = compare(1)

        # check if recognized name is in registered users
        if name in names:
            session['username'] = name
            if redirection == 'drinks':
                return redirect(url_for('drinks'))
            elif redirection == 'register':
                return redirect(url_for('register'))
            else:
                return redirect(url_for('index'))

        # check if face is not found or not registered user
        elif name == 'denied':
            return redirect(url_for('index'))

        # in case there is unrecognized output
        else:
            return "Error: User not in users when logging in."


# Logout route
@app.route('/logout')
def logout():
    # If there is session(cookie)
    if 'username' in session:
        # Delete session(cookie)
        session.pop('username', None)
        # Return to index route
        return redirect(url_for('index'))
    # If there is no session(cookie) go to index route
    else:
        # Return to index route
        return redirect(url_for('index'))


# Drink display route
# Order your drinks here
@app.route('/drinks')
def drinks():
    # Check if session(cookie) is set aka user is logged in
    if 'username' in session:
        # Get list of users
        result = dbi.read_query(dbq.USERS_NAMES)
        names = [i[0] for i in result]
        # Validate user against registered users (prevent malicious access)
        if session['username'] in names:
            # Set name variable to user name from session(cookie)
            name = session['username']
            # Query all drinks that can be made right now
            all_drinks = dbi.read_query(dbq.USERS_NAMES)
            return render_template('drinks.html', name=name, drinks=all_drinks)

        # Logged in user was not in user database (suspicious)
        else:
            return "Error: User not in users when accessing drinks."
    # User is not logged in. Redirect to index route
    else:
        return redirect(url_for('index'))


# Live feed route for camera display in html
# This feed is jpg image feed. Can be used as img source in HTML and CSS
@app.route('/live_feed')
def live_feed():
    # Return camera frames as jpg
    return Response(feed(video_camera), mimetype='multipart/x-mixed-replace; boundary=frame')


# TODO: ADD USER VALIDATION AND DRINK VALIDATION!
# Mix_drink route orders motor_controller to make drinks
# GETS: drink in drinks (drink name)
# SETS: recipe dict as response (pump_id, quantity)
@app.route('/mix_drink', methods=['GET', 'POST'])
def mix_drink():
    # Gets drink name as POST request
    drink = request.form.get('drink')
    # Gets recipe for drink as dict (pump_id, quantity)
    drink_recipe = dbi.read_query(dbq.AVAILABLE_RECIPE, drink)  # FIX: some unavailable drinks appear partially
    # TODO: Response for making drink and bolting to controller
    # Returns recipe for debugging or error. see line above
    return drink_recipe


# Route to register user form
@app.route('/register')
def register():
    # Validate login
    if 'username' in session:
        user = session['username']
        # FIX: needs to recognize admin to access
        # This is temporary way to make you admin
        if user == 'Niko Rintamäki':
            return render_template('register.html', name=user)
        # If not admin do nothing
        else:
            return redirect(url_for('index'))
    # If not logged in do nothing
    else:
        return redirect(url_for('index'))


@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    # Check if user session is set
    if 'username' in session:
        # Get list of users
        result = dbi.read_query(dbq.USERS_NAMES)
        names = [i[0] for i in result]
        # Validate session against registered users
        if session['username'] in names:
            name = session['username']
            all_drinks = dbi.read_query(dbq.ALL_DRINKS)
            ingredients = dbi.read_query(dbq.ALL_INGREDIENTS)
            drink_select = request.form.get('drink')
            drink_recipe = dbi.read_query(dbq.RECIPE, drink_select)
            return render_template('recipes.html', name=name, drink_select=drink_select, drinks=all_drinks,
                                   drink_recipe=drink_recipe, ingredients=ingredients)
        else:
            return "Error: User not in users when accessing drinks."
    else:
        return redirect(url_for('index'))


# TODO: working form. Flask-WTF?
@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    if 'username' in session:
        # Get list of users
        result = dbi.read_query(dbq.USERS_NAMES)
        names = [i[0] for i in result]
        # Validate session against registered users
        if session['username'] in names:
            result = request.form.to_dict()
            tolist = [v for k, v in result.items()]
            print(result)
            print(tolist)
            print('lol')
            return redirect(url_for('recipes'))
    else:
        return redirect(url_for('index'))


# Route for admins
@app.route('/admin')
def admin():
    # Check if user session is set
    # name = None
    if 'username' in session:
        # get list of users
        result = dbi.read_query(dbq.USERS_NAMES)
        names = [i[0] for i in result]
        # validate session against registered users
        if session['username'] in names:
            name = session['username']
            return render_template('admin.html', name=name)
        else:
            return "Error: User not in users when accessing admin."
    else:
        return redirect(url_for('index'))


# Register ny user
# GETS: name (plain user input)
# SETS: adds name, face_encoding and img_name(hashed md5) to Database
# SETS: saves photo to faces folder (hashed md5)
@app.route('/add_user', methods=['POST'])
def add_user():
    # username from POST
    username = request.form.get('username')
    admin = request.form.get('admin')
    # capture returns image path (md5)
    # capture takes photo of user and stores it into faces folder
    img_path = capture(username)
    # lear returns boolean
    # learn learns captured image and saves face mappings to database
    response = learn(username, img_path, admin)
    # IMPROVE: if face learned stay on page
    if response is True:
        return redirect(url_for('register'))
    else:
        return redirect(url_for('index'))


@app.route('/del_user', methods=['POST','GET'])
def del_user():
    if request.method == 'POST':
        usertodel = request.form.get('usertodel')
        response = dbi.read_query(dbq.DELETE_USER(usertodel))
        print(response)
    # username from POST
    all_users = dbq.USERS
    return  render_template('delete.html', all_users=all_users)
