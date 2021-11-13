from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.car import Car

@app.route('/add_car')
def add_car():
    return render_template('add_car.html')

@app.route('/edit_car/<int:id>')
def edit_car(id):
    data = {
        "id":id
    }
    car = Car.get_car(data) 
    return render_template('edit_car.html',car=car)

@app.route('/update_car/<int:id>',methods=["POST"])
def update_car(id):

    valid = Car.validate_car(request.form)
    if not valid:
        return redirect("/edit_car")
    
    data = {
        "car_id":id,
        "price":request.form["price"],
        "model":request.form["model"],
        "make":request.form["make"],
        "year":request.form["year"],
        "description":request.form["description"]
    }
    Car.update_car(data)
    return redirect("/dashboard")

@app.route('/submit_car',methods=["POST"])
def submit_car():

    valid = Car.validate_car(request.form)
    if not valid:
        return redirect("/add_car")
    
    data = {
        "price":request.form["price"],
        "model":request.form["model"],
        "make":request.form["make"],
        "year":request.form["year"],
        "description":request.form["description"],
        "sold":0,
        "seller_id":session["user_id"]
    }
    Car.add_car(data)
    return redirect("/dashboard")

@app.route('/view_car/<int:id>')
def view_car(id):
    data = {
        "id":id
    }
    car = Car.get_car(data)
    return render_template('view_car.html',car=car)

@app.route('/buy_car/<int:id>')
def buy_car(id):
    data = {
        "user_id":session["user_id"],
        "car_id":id
    }
    Car.buy_car(data)
    return redirect("/dashboard")

@app.route('/delete_car/<int:id>')
def delete_car(id):
    data = {
        "id":id
    }
    Car.delete_car(data)
    return redirect("/dashboard")

