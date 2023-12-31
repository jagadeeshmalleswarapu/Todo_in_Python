from flask import Flask, jsonify, make_response
from database import db
from auth import auth
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import base64

from notes import notes

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Notes.db'

paw = b'NTdtczdXMzExUTVtQl9oc3pfMkdmbTlzUkY2d19Ral8='
gethsh = base64.b64decode(paw).decode("utf-8")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://zmbcwodo:{gethsh}@rain.db.elephantsql.com/zmbcwodo'

# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://jagadeeshone:{gethsh}@dpg-cl6dkfiuuipc73cbcl9g-a.oregon-postgres.render.com/testdb_kf2t'

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
def home():
    return make_response(jsonify({
        "message": "Welcome to the home page!!!"
    }))


app.register_blueprint(auth)
app.register_blueprint(notes)

if __name__ == '__main__':
    app.run()
