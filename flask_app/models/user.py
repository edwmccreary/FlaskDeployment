from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.[class file name] import [class name]

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (email,first_name,last_name,password) VALUES (%(email)s,%(first_name)s,%(last_name)s,%(password)s)"
        return connectToMySQL("user_and_recipe").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("user_and_recipe").query_db(query,data)

        if len(user_db) < 1:
            return False
        
        return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        user_db = connectToMySQL("user_and_recipe").query_db(query,data)
        
        return cls(user_db[0])
