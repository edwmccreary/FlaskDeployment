from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.[class file name] import [class name]
from flask_app.models import car
from flask import flash
import re

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.cars = []
    
    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (email,first_name,last_name,password) VALUES (%(email)s,%(first_name)s,%(last_name)s,%(password)s)"
        return connectToMySQL("cars_db").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("cars_db").query_db(query,data)

        if len(user_db) < 1:
            return False
        
        return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users LEFT JOIN user_purchased_car ON users.id = user_purchased_car.user_id LEFT JOIN cars ON cars.id = user_purchased_car.car_id WHERE users.id = %(id)s"
        user_and_cars = connectToMySQL("cars_db").query_db(query,data)
        
        user = User(user_and_cars[0])
        if user_and_cars[0]["model"] is None:
            return user

        for row in user_and_cars:
            data = {
                "id":row['cars.id'],
                "price":row['price'],
                "model":row['model'],
                "make":row['make'],
                "year":row['year'],
                "description":row['description'],
                "created_at":row['created_at'],
                "updated_at":row['updated_at'],
                "seller_id":row['seller_id'],
                "sold":row['sold'],
                "owner":user
            }
            user.cars.append(car.Car(data))
        
        return user


    @staticmethod
    def validate_user(data):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        is_valid = True
        if len(data["first_name"]) < 3:
            flash("First Name cannot be less then 3 characters", "register")
            is_valid = False
        
        if len(data["last_name"]) < 3:
            flash("Last Name cannot be less then 3 characters", "register")
            is_valid = False
        
        if not email_reg.match(data["email"]):
            flash("invalid email", "register")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Your password must be atleast 8 characters in length", "register")
            is_valid = False

        return is_valid
