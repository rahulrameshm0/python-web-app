from flask import render_template, flash, redirect, url_for
from main import app, db, bcrypt
from main.forms import RegistrationForm,LoginForm
from main.models import User, Post
from flask_login import login_user, current_user,logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.user_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! now, you are able to login", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form = form)

@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("incorrect email or password", "danger")
    return render_template("login.html", title = 'Login', form = form)

@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=["GET","POST"])
def account():
    return render_template("account.html", title='Account')