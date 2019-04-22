from flask import Flask
from flask_restful import Api
from resources.register import Register, Edit


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mindsy-cadastro-microservice'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Register, '/register')
api.add_resource(Edit, '/edit/<int:id>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')