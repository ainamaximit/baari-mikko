from flask import Flask, render_template, request, Response, redirect, session, url_for
from facecam import compare, camera_feed, capture, learn
from db_query import get_all_drinks, get_availble_recipe, get_users_names, get_recipes, get_recipe

app = Flask(__name__, static_url_path='/static')
# key for sessions(cookie)
app.secret_key = 'penis'

# Index route at start whith two differet route names
@app.route('/')
@app.route('/index')
def index():
    # check if user session is set
    name = None
    if 'username' in session:
        # get list of users
        names = get_users_names()
        # validate session agains registered users
        if session['username'] in names:
            name = session['username']
    return render_template('index.html', name=name)

# Login route with optional redirection.
@app.route('/login/<redirection>')
@app.route('/login')
def login(redirection=None):
    # get list of users
    names = get_users_names()
    # check if user session is set
    if 'username' in session:
        # validate session agains registered users
        if session['username'] in names:
            if redirection == 'drinks':
                return redirect(url_for('drinks'))
            elif redirection == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return redirec(url_for('logout'))

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

        # in case there is unrocnized output
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
    name = None
    if 'username' in session:
        # Get list of users
        names = get_users_names()
        # Validate user against registered users (prevent malicious access)
        if session['username'] in names:
            # Set name variable to user name from session(cookie)
            name = session['username']
            # Query all drinks that can be made right now
            drinks = get_all_drinks()
            return render_template('drinks.html', name=name, drinks=drinks)

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
    return Response(camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


### FIX: ADD USER VALIDATION AND DRINK VALIDATION! ###
# Mix_drink route orders motor_controller to make drinks
# GETS: drink in drinks (drink name)
# SETS: recipe dict as response (pump_id, quantity)
@app.route('/mix_drink', methods=['GET','POST'])
def mix_drink():
    # Gets drink name as POST request
    drink = request.form.get('drink')
    # Gets recipe for drink as dict (pump_id, quantity)
    drink_recipe = get_availble_recipe(drink) # FIX: some unavailable drinks appear partially
    # TODO: Response for making drink and bolting to controller
    # Returns recipe for debuggin or error. see line above
    return drink_recipe

# Route to registe user form
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

@app.route('/recipes', methods=['GET','POST'])
def recipes():
    # Check if user session is set
    name = None
    if 'username' in session:
        # Get list of users
        names = get_users_names()
        # Validate session agains registered users
        if session['username'] in names:
            name = session['username']
            drinks = get_all_drinks()
            drink_select = request.form.get('drink')
            drink_recipe = get_recipe(drink_select)
            return render_template('recipes.html', name=name, drink_select=drink_select, drinks=drinks, drink_recipe=drink_recipe)
        else:
            return "Error: User not in users when accessing drinks."
    else:
        return redirect(url_for('index'))

# Route for admins
@app.route('/admin')
def admin():
    # Check if user session is set
    name = None
    if 'username' in session:
        # get list of users
        names = get_users_names()
        # validate session agains registered users
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
    # capture returns image path (md5)
    # capture takes photo of user and stores it into faces folder
    img_path = capture(username)
    # lear returns boolean
    # learn learns captured image and saves face mappings to database
    response = learn(username, img_path)
    # IMPROVE: if face learned stay on page
    if response == True:
        return redirect(url_for('register'))
    else:
        return redirect(url_for('index'))

# TODO: store recipe or update it
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    print('recipe to make')
