from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/home')
def home():
    users = User.query.all()
    return render_template("home.html", users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081,debug=True)