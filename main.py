from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,  LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "0000"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}','{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.id}', '{self.title}','{self.date_posted}'"
   
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

if __name__ == "__main__":
    app.run(debug=True)


