from flask import Blueprint, request, jsonify, make_response
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post('/register')
def register():
    email = request.json['email']
    password = request.json['password']

    if not email or not password:
        return make_response(jsonify({
            "error": "email and password should not be empty"
        })), 400
    if not validators.email(email):
        return make_response(jsonify({
            "error": "Please enter a valid email"
        })), 400

    if len(password) < 3:
        return make_response(jsonify({
            "error": "Password should be more than 3 characters"
        })), 400

    gen_pwd_hash = generate_password_hash(password=password)

    user = User(email=email, password=gen_pwd_hash)
    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({
        "message": "User registered successfully",
        "email": email
    })), 201


@auth.post('/login')
def login():
    email = request.json['email']
    password = request.json['password']

    if not email or not password:
        return make_response(jsonify({
            "error": "email and password should not be empty"
        })), 400
    if not validators.email(email):
        return make_response(jsonify({
            "error": "Please enter a valid email"
        })), 400

    if len(password) < 3:
        return make_response(jsonify({
            "error": "Password should be more than 3 characters"
        })), 400

    user = User.query.filter_by(email=email).first()
    if user:
        un_hash_pwd = check_password_hash(user.password, password)
        if un_hash_pwd:
            access = create_access_token(user.id)
            refresh = create_refresh_token(user.id)

            return make_response(jsonify({
                "message": "user login successfully",
                "email": user.email,
                "access": access,
                "refresh": refresh
            })), 200

    return make_response(jsonify({
        "error": "Invalid credentials"
    })), 401


@auth.get('/')
@jwt_required()
def default_auth():
    try:
        user_data = User.query.all()
        data = []
        for items in user_data:
            data.append(items.email)

        return make_response(jsonify({
            "data": data
        })), 200
    except Exception as e:
        return make_response(jsonify({
            'error': f'Exception: {e}'
        })), 500

