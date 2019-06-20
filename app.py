from flask import Flask
from flask_restful import Api
from resources.register import RegisterPsychologist
from resources.edit import EditPsychologist
from resources.delete import DeleteUser
from resources.user_information import ShowPsychologistInformationCRP
from resources.token import TokenInformation
from flask_cors import CORS
from db import db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db3mp2dauwixvkcg:t3hkuoethj9xvd1l@u0zbt18wwjva9e0v.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/w63zlckiy2z278iv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
CORS(app)


api.add_resource(RegisterPsychologist, '/psychologist')
api.add_resource(EditPsychologist, '/psychologist/<string:crp>')
api.add_resource(DeleteUser, '/psychologist/<string:crp>')
api.add_resource(ShowPsychologistInformationCRP, '/psychologist/<string:crp>')
api.add_resource(TokenInformation, '/psychologist/token/<string:crp>')


db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

