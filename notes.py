from flask import Blueprint, make_response, jsonify, request
from database import Notes, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

notes = Blueprint('notes', __name__, url_prefix='/notes')


@notes.get('/')
def notes_home():
    return make_response(jsonify({
        "message": "hello!!!"
    }))


@notes.post('/add')
@jwt_required()
def add_notes():
    user_id = get_jwt_identity()
    note = request.json['note']
    if len(note) < 10:
        return make_response(jsonify({
            "error": "Please enter more than 10 characters"
        })), 400

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response(jsonify({
            "error": "Unknown User, Please register or create the user first"
        })), 400
    note_db = Notes(note=note, user_id=user_id)
    db.session.add(note_db)
    db.session.commit()

    user_len_find = Notes.query.filter_by(user_id=user_id).all()
    len_notes = len(user_len_find)

    return make_response(jsonify({
        "message": f"Hi {user.username}, notes-{len_notes} has been added to your account"
    })), 201


@notes.get('/all')
@jwt_required()
def get_all():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response(jsonify({
            "error": "User not found"
        })), 404

    note = Notes.query.filter_by(user_id=user_id).all()

    if not note:
        return make_response(jsonify({
            "error": "Notes are empty, Please add the notes"
        })), 404

    data = []

    for n in note:
        data.append({
            "notes_id": n.id,
            "notes": n.note,
            "created_at": n.created_at,
            "update_at": n.updated_at,
            "user": user.username
        })

    return make_response(jsonify({
        'data': data
    })), 200


@notes.get('/<int:id>')
@jwt_required()
def get_one(id):
    user_id = get_jwt_identity()

    note = Notes.query.filter_by(user_id=user_id, id=id).first()

    if not note:
        return make_response(jsonify({
            "error": "Notes not available"
        })), 404

    return make_response(jsonify({
        "note": note.note
    })), 200


@notes.put('/<int:id>')
@notes.patch('/<int:id>')
@jwt_required()
def update_notes(id):
    note_json = request.json['note']
    user_id = get_jwt_identity()

    note = Notes.query.filter_by(id=id, user_id=user_id).first()
    if not note:
        return make_response(jsonify({
            "error": "Notes not found"
        })), 404
    if len(note_json) < 5:
        return make_response(jsonify({
            "error": "Please enter more than 5 characters"
        })), 400
    note.note = note_json
    db.session.commit()

    return make_response(jsonify({
        "note": note.note
    })), 200


@notes.delete('/<int:id>')
@jwt_required()
def delete_notes(id):
    user_id = get_jwt_identity()

    note = Notes.query.filter_by(id=id, user_id=user_id).first()
    if not note:
        return make_response(jsonify({
            "error": "Notes not found"
        })), 404
    temp_id = id
    db.session.delete(note)
    db.session.commit()
    return make_response(jsonify({
        "message": f"{temp_id} has been deleted"
    }))
