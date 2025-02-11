from flask import render_template, flash, redirect, url_for
from main import app
from main.forms import RegistrationForm,LoginForm
from main.models import User, Post

posts = [
    {"author": "Rahul",
     "title": "blog post 1",
     "content":"first post content",
     "date":"April, 1, 2005"
     },
    {"author": "Jonny",
     "title": "blog post 2",
     "content":"second post content",
     "date":"April, 1, 2005"
     }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Accounct successfully created for {form.user_name.data}!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", title='register', form = form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "jo@gmail.com" and form.password.data == "password":
            flash("login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("incorrect email or password", "danger")
    return render_template("login.html", title = 'Login', form = form)