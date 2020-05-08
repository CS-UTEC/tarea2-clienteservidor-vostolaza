from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#CRUD users

#=================================================================================#

#1. CREATE
@app.route('/users', methods=['POST'])
def create_user():
    #1. Create user object
    body = json.loads(request.data)
    user = entities.User(
        username = body['username'],
        name = body['name'],
        fullname = body['fullname'],
        password = body['password']
    )

    #2. Send user to persistence layer
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    #3. Send response to client
    message = {'msg': 'User Created'}
    json_message = json.dumps(message, cls = connector.AlchemyEncoder)
    res = Response(json_message, status=201, mimetype='application/json')
    return res


#2. READ
@app.route('/users', methods=['GET'])
def read_user():
    #1. Consult database for all users
    db_session = db.getSession(engine)
    response = db_session.query(entities.User)

    #2. Convert all users into JSON
    users = response[:]
    json_message = json.dumps(users, cls = connector.AlchemyEncoder)

    #3. Send response to client
    res = Response(json_message, status=201, mimetype='application/json')
    return res

#3. UPDATE
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    #1. Search db for user with matching id
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).first()

    #2. Update user data
    body = json.loads(request.data)
    for key in body.keys():
        setattr(user, key, body[key])

    #3. Saving the update into the database
    db_session.add(user)
    db_session.commit()

    #4. Send response to client
    message = {'msg' : 'User updated'}
    json_message = json.dumps(message, cls = connector.AlchemyEncoder)
    return Response(json_message, status = 201, mimetype='application/json')

#4. DELETE
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    #1. Search db for user with matching id
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).first()

    #2. Delete user from database
    db_session.delete(user)
    db_session.commit()

    #3. Send response to client
    message = {'msg' : 'Users deleted'}
    json_message = json.dumps(message, cls = connector.AlchemyEncoder)
    return Response(json_message, status = 201, mimetype = 'application/json')
#=================================================================================#


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
