from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re

class Car:
    def __init__(self,data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.seller_id = data["seller_id"]
        self.sold = data["sold"]
        self.owner = None
    
    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars JOIN users ON cars.seller_id = users.id"
        cars_db = connectToMySQL("cars_db").query_db(query)
        cars = []

        for row in cars_db:
            car = Car(row)
            data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"]
            }
            car.owner = user.User(row)
            cars.append(car)
        
        return cars
    
    @classmethod
    def get_car(cls,data):
        query = "SELECT * FROM cars JOIN users ON cars.seller_id = users.id WHERE cars.id = %(id)s"
        cars_db = connectToMySQL("cars_db").query_db(query,data)
        row = cars_db[0]
        car = Car(row)
        data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"]
            }
        car.owner = user.User(row)
        return car
        

    @classmethod
    def add_car(cls,data):
        query = "INSERT INTO cars (price,model,make,year,description,seller_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(seller_id)s)"
        return connectToMySQL("cars_db").query_db(query,data)
    
    @classmethod
    def update_car(cls,data):
        query = "UPDATE cars SET model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s, price=%(price)s WHERE id = %(car_id)s"
        return connectToMySQL("cars_db").query_db(query,data)

    @classmethod
    def delete_car(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s"
        return connectToMySQL("cars_db").query_db(query,data)
    
    @classmethod
    def buy_car(cls,data):
        query = "INSERT INTO user_purchased_car (user_id,car_id) VALUES (%(user_id)s,%(car_id)s)"
        connectToMySQL("cars_db").query_db(query,data)
        query = "UPDATE cars SET sold=1 WHERE id = %(car_id)s"
        return connectToMySQL("cars_db").query_db(query,data)

    @staticmethod
    def validate_car(data):
        is_valid = True
        if float(data["price"]) <= 0:
            flash("Car must have a Price")
            is_valid = False
        if len(data["year"]) > 0:
            if int(data["year"]) <= 0:
                flash("Car must have a Year")
                is_valid = False
        if len(data["year"]) < 1:
            flash("Car must have a Year")
            is_valid = False
        
        if len(data["model"]) < 1:
            flash("Car must have a model")
            is_valid = False
        if len(data["make"]) < 1:
            flash("Car must have a make")
            is_valid = False
        if len(data["description"]) < 1:
            flash("Car must have a description")
            is_valid = False
        return is_valid
    

    

