# import os
# from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from resources.register import RegisterPsychologist
from resources.edit import EditPsychologist
from resources.delete import DeleteUser
from resources.user_information import ShowPsychologistInformationID

app = Flask(__name__)
# load_dotenv(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost:3306/MINDSY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mindsy'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterPsychologist, '/psychologist')
api.add_resource(EditPsychologist, '/psychologist/<string:crp>')
api.add_resource(DeleteUser, '/psychologist/<int:id>')
api.add_resource(ShowPsychologistInformationID, '/psychologist/<string:crp>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')