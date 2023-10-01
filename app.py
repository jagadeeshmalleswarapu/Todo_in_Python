from flask import Flask, jsonify, make_response
from database import db
from auth import auth
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from notes import notes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Notes.db'
app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"
CORS(app=app, origins=['*'])

# cors = CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"])

db.app = app
db.init_app(app=app)
JWTManager(app=app)


@app.get('/create_db')
def create_db():
    db.create_all()
    return make_response(jsonify({
        "date": "db created successfully"
    }))


@app.get('/')
@cross_origin()
def home():
    return make_response(jsonify({
        "message": "Welcome to the home page!!!"
    }))


app.register_blueprint(auth)
app.register_blueprint(notes)

if __name__ == '__main__':
    app.run(debug=True)
