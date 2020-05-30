"""Flask app for Feedback Project"""
from flask import Flask, request, redirect, render_template, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUserForm, LogInUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# run this line of code on the command line to create the table only once
# db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home_page():
    """Redirects to /register"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Show a form that when submitted will register/create a user."""
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = user.username
        flash("You have Sucessfully Created Your Account")
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/users/<username>")
def user_detail_page(username):
    """Redirects to user detail page"""
    if "username" not in session:
        flash("Please login first!")
        return redirect("/login")
    else:
        user = User.query.get(username)
    return render_template("user_detail.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def logIn_user():
    """Show a form that when submitted will log in an existing user."""
    form = LogInUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate user
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back {user.username}!")
            session["username"] = user.username
            return redirect(f"/users/<username>")
        else:
            form.username.errors = ["Invalid name/password"]
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    flash("You are now logged out!")
    return redirect("/")
