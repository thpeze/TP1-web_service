from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime
from flask import Flask, jsonify

 
db_string = "postgresql://root:root@localhost:5432/postgres"
 
engine = create_engine(db_string)

app=Flask(__name__)

data=[]

@app.route("/home", methods=["GET"])
def get_users():
    users = run_sql_with_results("SELECT * FROM users")
    date = []
    for row in users:
        user = {
            "id":row[0],
            "firstname":row[1],
            "lastname":row[2],
            "age":row[3],
            "email":row[4],
            "job":row[5]
        }
        data.append(user)
    return jsonify(data)

def get_application():
    application = run_sql_with_results("SELECT * FROM application")
    date = []
    for row in application:
        user = {
            "id":row[0],
            "appname":row[1],
            "username":row[2],
            "lastconnection":row[3]
        }
        data.append(user)
    return jsonify(data)




create_user_table_sql = text("""
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    age INTEGER,
    email VARCHAR(255) UNIQUE NOT NULL,
    job VARCHAR(255)
)
""")
 
create_application_table_sql = text("""
CREATE TABLE IF NOT EXISTS application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    lastconnection TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
)
""")
 
 
def run_sql1(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(query)
        trans.commit()

def run_sql(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text(query))  # Create a text object here
        trans.commit()



def run_sql_with_results(query:str):
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(text(query))
        trans.commit()
        return result
        


 

fake = Faker()

def populate_tables():
    apps=['FACEBOOK','INSTAGRAM','TWITTER','SNACHAT','TIKTOK']
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18,50)
        email = fake.email()
        job = fake.job().replace("'","")

        insert_user_query= f"""
            INSERT INTO users (firstname, lastname, age, email, job)
            VALUES ('{firstname}','{lastname}','{age}','{email}','{job}')
            RETURNING id
        """
        user_id = run_sql_with_results(insert_user_query).scalar()

        username = fake.user_name()
        lastconnection = datetime.now()
        app_name = random.choice(apps)

        insert_application_query = f"""
            INSERT INTO application (appname, username, lastconnection, user_id)
            VALUES ('{app_name}', '{username}', '{lastconnection}', '{user_id}')
            RETURNING id
        """
        run_sql(insert_application_query)



        datetime.now()





if __name__ =='__main__':
    #Create user table
    run_sql1(create_user_table_sql)
    #Create Application table
    run_sql1(create_application_table_sql)
    populate_tables()

app.run(host='0.0.0.0', port=8081, debug=True)