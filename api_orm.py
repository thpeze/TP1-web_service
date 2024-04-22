from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    job = db.Column(db.String(100))

    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.TIMESTAMP)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('applications', lazy=True))

    def __init__(self, appname, username, lastconnection, user_id):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection
        self.user_id = user_id



def populate():
    apps=['FACEBOOK','INSTAGRAM','TWITTER','SNACHAT','TIKTOK']
    fake = Faker()
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randint(18, 50)
        email = fake.email()
        job = fake.job()

        user = User(firstname=firstname, lastname=lastname, age=age, email=email, job=job)
        db.session.add(user)
        db.session.commit()

        for _ in range(5):  # Créer quelques applications pour chaque utilisateur
            appname = random.choice(apps)
            username = fake.user_name()
            lastconnection = datetime.now()
            application = Application(appname=appname, username=username, lastconnection=lastconnection, user_id=user.id)
            db.session.add(application)
            db.session.commit()

        datetime.now()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate()
    app.run(debug=True)



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'age': user.age, 'email': user.email, 'job': user.job} for user in users])






@app.route('/users', methods=['POST'])
def create_user():
    data = request.json 
    user = User(firstname=data['firstname'], lastname=data['lastname'], age=data['age'], email=data['email'], job=data['job'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'id': user.id}), 201



@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json 
    user.firstname = data.get('firstname', user.firstname)
    user.lastname = data.get('lastname', user.lastname)
    user.age = data.get('age', user.age)
    user.email = data.get('email', user.email)
    user.job = data.get('job', user.job)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200



@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
