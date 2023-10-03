from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Emids123@localhost/test'

db = SQLAlchemy(app)


class UserFlask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.get('/create_db')
def db_cre():
    db.create_all()
    return {"data": "db created"}


if __name__ == '__main__':
    app.run(debug=True)
