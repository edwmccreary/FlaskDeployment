from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
# from flask_app.models.[name of class file] import [class name]
from flask_app.models.user import User
from flask_app.models.validate import Validate
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# put your app.route logic here:

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register',methods=["POST"])
def register():
    
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":request.form["password"]
    }
    validate = Validate.registration(data)
    if not validate:
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data["password"] = pw_hash

    if request.form["password"] != request.form["password_confirm"]:
        flash("Password and Confirm password do not match", "register")
        return redirect("/")
    
    if User.get_by_email(data):
        flash("A User is already registered for this email", "register")
        return redirect("/")
    
    User.insert_user(data)
    return redirect("/")

@app.route('/login',methods=["POST"])
def login():
    data = {
        "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email/Password", "login")
        return redirect("/")
    
    session["user_id"] = user_in_db.id

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in", "login")
        return redirect("/")
    else:
        data = {
            "id":session["user_id"]
        }
        user = User.get_user(data)
        recipes = Recipe.get_all_recipes(data)
        return render_template("dashboard.html",user=user,recipes=recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")