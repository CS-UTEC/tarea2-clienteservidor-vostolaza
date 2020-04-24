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

@app.route('/palindrome/<palabra>')
def palindromo(palabra):
    j = 0
    for i in range(len(palabra)-1, 0, -1):
        if palabra[i] != palabra[j]:
            return "No es un palindromo"
        j = j + 1
    return "Es un palindromo"

@app.route('/multiplo/<numero1>/<numero2>')
def multiplo(numero1, numero2):
    if int(numero2) % int(numero1) == 0:
        return f'{numero1} es multiplo de {numero2}'
    else:
        return f'{numero1} no es multiplo de {numero2}'

@app.route('/esprimo/<num>')
def esPrimo(num):
    for i in range(2, int(int(num)/2)):
        if int(num)%i == 0:
            return "No es primo"
    return "Es primo"

@app.route('/create_user/<nombre>/<apellido>/<usrname>/<pwd>')
def create_user(nombre, apellido, usrname, pwd):
    user = entities.User(
        name = nombre,
        fullname = apellido,
        password = pwd,
        username = usrname
    )
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return f'User created:<br><h2>Nombre: {nombre}<br>Apellido: {apellido}<br>Username: {usrname}<br>Password: {pwd}</h2>' 

@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    # retStr = ''
    # for i in range(len(users)):
    #     temp_str = f'<h2>User {i}:</h2><br><b>Nombre: {users[i].name}<br>Apellido: {users[i].fullname}<br>Username: {users[i].username}<br>Password: {users[i].password}</h2>'
    #     retStr = retStr+'<br>'+temp_str
    # return retStr

    retStr = '<table>'
    for i in range(len(users)):
        temp_str = f'<tr><td>{users[i].name}</td><td>{users[i].fullname}</td><td>{users[i].username}</td><td>{users[i].password}</td></tr>'
        retStr = retStr + temp_str
    retStr = retStr + '</table>'
    return retStr

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
