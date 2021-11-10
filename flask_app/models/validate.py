from flask import flash
import re

class Validate:
    @staticmethod
    def registration(data):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        is_valid = True
        if len(data["first_name"]) < 1:
            flash("First Name cannot be blank", "register")
            is_valid = False
        
        if len(data["last_name"]) < 1:
            flash("Last Name cannot be blank", "register")
            is_valid = False
        
        if not email_reg.match(data["email"]):
            flash("invalid email", "register")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Your password must be atleast 8 characters in length", "register")
            is_valid = False

        return is_valid