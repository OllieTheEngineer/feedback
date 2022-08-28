from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User
from forms  import RegisterForm, LoginForm, FeedbackForm, DeleteForm

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
        if user:
            session["username"] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("users/login.html", form=form)
    return render_template("users/login.html", form=form)

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

@app.route("/users/<username>")
def show_info(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show_user.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    # if username is not saved in session or the username does not match the username in session return unauthorized
    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    # retrieve username
    user = User.query.get(username)
    # delete retrieved user
    db.session.delete(user)
    # finalize deletion
    db.session.commit()
    # remove username from saved user
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )

        db.session.add(feedback)
        db.session.commit()


        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", form=form)

