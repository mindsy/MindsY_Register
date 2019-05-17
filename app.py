from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.register import RegisterPsychologist, UserLogin, TokenRefresh, UserLogout
from resources.edit import EditPsychologist
from resources.delete import DeleteUser
from resources.user_information import ShowPsychologistInformationID
from blacklist import BLACKLIST

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'mindsy-cadastro-microservice'
app.config['JWT_SECRET_KEY'] = 'mindsy-microservice-register'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        'discription': 'The token has expired',
        'error': 'token_expired'
    }), 401    

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'discription': 'Signature verification failed.',
        'error': 'Invalid token.'
    }), 401

@jwt.unauthorized_loader
def token_not_fresh_callback(error):
    return jsonify({
        'discription': 'The token is not fresh.',
        'error': 'Fresh token required'
    }), 401

@jwt.needs_fresh_token_loader
def missing_token_callback():
    return jsonify({
        'discription': 'Request does not contain an access token.',
        'error': 'Authorization required.'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'discription': 'The token has been revoked.',
        'error': 'token revoked'
    }), 401


api.add_resource(RegisterPsychologist, '/register-psychologist')
api.add_resource(EditPsychologist, '/edit-psychologist/<string:crp>')
api.add_resource(DeleteUser, '/delete-user/<int:id>')
api.add_resource(ShowPsychologistInformationID, '/psychologist_information/<string:crp>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')