from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms  import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)
        
        db.session.add(user)
        session['username'] = user.username
        db.session.commit()

        return redirect("/secret")
    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=["GET","POST"])
def user_login():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        return redirect('/secret')
@app.route('/secret', methods=['GET'])
def secrets():

    if "username" in session:
        return flash("'You made it!' (Don't worry, we'll get rid of this soon!'")
    else:
        return render_template("secrets.html")

@app.route('/logout')
def logout():

    session.pop("username")

    return redirect("/")

# @app.route("/users/<username>")
# def show_info(username):

