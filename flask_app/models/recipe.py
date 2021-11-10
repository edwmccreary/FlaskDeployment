from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.under_thirty = data["under_thirty"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipe_date = data["recipe_date"]
        self.user_id = data["user_id"]
    
    @classmethod
    def add_recipe(cls,data):
        query = "INSERT INTO recipes (name,description,under_thirty,instructions,recipe_date,user_id) VALUES (%(name)s,%(description)s,%(under_thirty)s,%(instructions)s,%(recipe_date)s,%(user_id)s)"
        return connectToMySQL("user_and_recipe").query_db(query,data)

    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s"
        recipe_db = connectToMySQL("user_and_recipe").query_db(query,data)
        
        return cls(recipe_db[0])

    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM recipes WHERE user_id=%(id)s ORDER BY id DESC"
        recipe_db = connectToMySQL("user_and_recipe").query_db(query,data)
        recipes = []

        for recipe in recipe_db:
            recipes.append(cls(recipe))
        
        return recipes

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, under_thirty=%(under_thirty)s, recipe_date=%(recipe_date)s, instructions=%(instructions)s WHERE id = %(id)s"
        return connectToMySQL("user_and_recipe").query_db(query,data)
    
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("user_and_recipe").query_db(query,data)