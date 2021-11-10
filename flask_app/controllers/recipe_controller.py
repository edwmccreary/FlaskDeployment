from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/recipe/<int:id>")
def view_recipe(id):
    data = {
        "id":id
    }
    recipe = Recipe.get_recipe(data)
    data = {
            "id":session["user_id"]
        }
    user = User.get_user(data)
    return render_template("recipe.html",recipe=recipe,user=user)

@app.route("/create_recipe")
def create_recipe():
    return render_template("create_recipe.html")

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    data = {
        "name":request.form["name"],
        "description":request.form["description"],
        "under_thirty":request.form["under_thirty"],
        "instructions":request.form["instructions"],
        "recipe_date":request.form["recipe_date"],
        "user_id":session["user_id"]
    }
    Recipe.add_recipe(data)
    return redirect("/dashboard")

@app.route("/edit_recipe/<int:id>")
def edit_recipe(id):
    data = {
        "id":id
    }
    recipe = Recipe.get_recipe(data)
    data = {
            "id":session["user_id"]
        }
    user = User.get_user(data)
    return render_template("edit_recipe.html",recipe=recipe,user=user)

@app.route("/update_recipe/<int:id>",methods=["POST"])
def update_recipe(id):
    data = {
        "id":id,
        "name":request.form["name"],
        "description":request.form["description"],
        "under_thirty":request.form["under_thirty"],
        "instructions":request.form["instructions"],
        "recipe_date":request.form["recipe_date"],
        "user_id":session["user_id"]
    }
    Recipe.update_recipe(data)
    return redirect("/dashboard")

@app.route("/recipe_delete/<int:id>")
def delete_recipe(id):
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")