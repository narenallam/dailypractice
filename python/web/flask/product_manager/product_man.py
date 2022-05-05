# Product Management API

import uuid
import datetime
from functools import wraps

import jwt
from werkzeug.security import (generate_password_hash,
                               check_password_hash)

from flask import (Flask,
                   request,
                   jsonify,
                   make_response)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select


# Flask Application
app = Flask(__name__)

# App Configuration - Shouldnot be hard coded
app.config['SECRET_KEY'] = '497a24dbcecaee8c1dfa84f3a5818f3f'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://naren:Python123@192.168.161.128/classicmodels"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# mapps all tables to ORM classes
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Users = Base.classes.users
Employees = Base.classes.employees


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session = Session(engine)
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = session.query(Users).filter_by(public_id=data['public_id']).first()
        except Exception as ex:
            return jsonify({'message': 'token is invalid', "error": str(ex)})

        return f(current_user, *args, **kwargs)
    return wrapper


@app.route('/register', methods=['POST'])
def signup_user(): 
    session = Session(engine)
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    is_admin = True if data['is_admin'] == True else False
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=is_admin)
    session.add(new_user) 
    session.commit()   
    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST']) 
def login_user():
    session = Session(engine)
    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   # user = Users.query.filter_by(name=auth.username).first()
    user = session.query(Users).filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id,
                           'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, 
                           app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route("/addemployee", methods=['POST'])
@token_required
def insert_emps():
    reponse = {}
    try:
        #inserting a record into employees table
        session = Session(engine)
        emp_data = request.json
        session.add(Employees(**emp_data))
        session.commit()
        reponse["message"] = "Data successfully added!"
    except Exception as ex:
        reponse["error"] = str(ex)
        
    return jsonify(reponse)

@app.route("/getemployee", methods=['GET'])
@token_required
def get_emp(current_user):
    reponse = {}
    try:
        #inserting a record into employees table
        session = Session(engine)
        employee = session.query(Employees).first()
        reponse["data"] = { "Full Name": employee.firstName + " " + employee.lastName}
    except Exception as ex:
        reponse["error"] = str(ex)
        
    return jsonify(reponse)

@app.route("/getall", methods=['GET'])
@token_required
def get_emps(current_user):
    reponse = {}
    try:
        #inserting a record into employees table
        session = Session(engine)
        _ids = request.json["ids"]
        stmt = select(Employees).where(Employees.employeeNumber.in_(_ids))
        reponse["data"] = [emp.firstName + " " + emp.lastName for emp in session.scalars(stmt)]
    except Exception as ex:
        reponse["error"] = str(ex)
        
    return jsonify(reponse)

if __name__ == '__main__':
    app.run(debug=True)