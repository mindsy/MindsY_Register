from flask import Flask
from flask_restful import Api

from resources.register import RegisterPsychologist
from resources.edit import EditPsychologist
from resources.delete import DeleteUser
from resources.user_information import ShowPsychologistInformationCRP
from flask_cors import CORS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db3mp2dauwixvkcg:t3hkuoethj9xvd1l@u0zbt18wwjva9e0v.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/w63zlckiy2z278iv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterPsychologist, '/psychologist')
api.add_resource(EditPsychologist, '/psychologist/<string:crp>')
api.add_resource(DeleteUser, '/psychologist/<string:crp>')
api.add_resource(ShowPsychologistInformationCRP, '/psychologist/<string:crp>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')

