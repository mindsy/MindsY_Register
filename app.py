import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.register import RegisterPsychologist
from resources.edit import EditPsychologist
from resources.delete import DeleteUser
from resources.user_information import ShowPsychologistInformationID

app = Flask(__name__)
load_dotenv(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
#'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get("APP_SECRET_KEY")
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(RegisterPsychologist, '/register-psychologist')
api.add_resource(EditPsychologist, '/edit-psychologist/<string:crp>')
api.add_resource(DeleteUser, '/delete-user/<int:id>')
api.add_resource(ShowPsychologistInformationID, '/psychologist-information/<string:crp>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')