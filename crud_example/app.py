from crypt import methods
import mimetypes
from operator import methodcaller
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

#examples from: https://www.youtube.com/watch?v=WDpPGFkI9UU&t=23s&ab_channel=ProgramandoComRoger

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/youtube'

db = SQLAlchemy(app)

#select all
#select one
#insert
#update
#delete

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return{"id": self.id, "nome": self.nome, "email": self.email}

# db.create_all() #creates table at db 

def generate_response(status, content_name, content, mesages = False):
    body = {}
    body[content_name] = content

    if(mesages):
        body[mesages] = mesages

    return Response(json.dumps(body), status=status,  mimetype='application/json')

@app.route('/usuarios', methods=['GET'])
def select_users():
    users_object = Usuario.query.all()
    users_json = [user.to_json() for user in users_object]

    return generate_response(200, 'usuarios', users_json, 'ok' )

@app.route('/usuario/<id>')
def select_user(id):
    user_object = Usuario.query.filter_by(id = id).first()
    user_json = user_object.to_json()

    return generate_response(200, 'usuario', user_json)

#stopped at 17'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3022, debug = True)
