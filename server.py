from flask_app import app
# import all of your controllers into here
# from flask_app.controllers import [name of controller file]
from flask_app.controllers import user_controller
from flask_app.controllers import car_controller

if __name__=="__main__":
    app.run(debug=True)