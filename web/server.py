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


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
