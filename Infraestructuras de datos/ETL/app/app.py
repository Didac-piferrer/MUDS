import json
import requests
import time
import hashlib
from flask import Flask, json, Response, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from dataclasses import dataclass

#CLASSES 
@dataclass
class ConnectionMongoDB:
    server: str
    port: str
    username: str
    password: str
    db: str

    def getDB(self):
        mongoClient = MongoClient("mongodb://" + 
                        str(self.username) + ":" + 
                        str(self.password) + "@" + 
                        str(self.server) + ":" + 
                        str(self.port) + 
                        "/?authMechanism=DEFAULT&authSource=" + 
                        str(self.db), serverSelectionTimeoutMS=500)
        try:
            if mongoClient.admin.command('ismaster')['ismaster']:
                return True, mongoClient
            
        except OperationFailure:
            return False, "Database not found."
        
        except ServerSelectionTimeoutError:
            return False, "MongoDB Server is down."

@dataclass
class Superhero:
    nombre: str
    descripcion: str
    comics: int
    series: int
    historias: int
    eventos: int

    def toDBCollection (self):
        return {
            "nombre":self.nombre,
            "descripcion": self.descripcion,
            "comics":self.comics,
            "series": self.series,
            "historias": self.historias,
            "eventos": self.eventos
        }
 
#GLOBAL VARIABLES
app = Flask(__name__)
#DB_NAME = "db_crashell"
#DB_SERVER = "cs_mongodb"
#DB_USER = "root-crashell"
#DB_PASS = "password-crashell"
#DB_PORT = '27017'

DB_NAME = "db_hero"
DB_SERVER = "my_mongo"
DB_USER = "didac"
DB_PASS = '12345'
DB_PORT = '27017'


#Custom Hereos for testing
MisSuperheros = [
    Superhero("Juan", "mortal",23, 3, 6, 6),
    Superhero("Julio", "lento",254, 2, 41, 2),
    Superhero("Cesar", "rapido",2355, 3, 49, 1),
    Superhero("Patroclo", "inutil",234, 9, 43, 8)
]

#PUBLIC FUNCTIONS

def getMongoClient():
    return ConnectionMongoDB(DB_SERVER,DB_PORT,DB_USER,DB_PASS,DB_NAME).getDB()

def getCollection(connection,collection_name):
    db = connection[DB_NAME]
    return db[collection_name]

#FLASK ROUTES

@app.route('/api-insertar')
def get_api():
    ok, connection = getMongoClient()
    if not ok:
        return Response(response=json.dumps(connection), mimetype='application/json')
    collection = getCollection(connection,"superheros")

    for sh in MisSuperheros:
        collection.insert_one(sh.toDBCollection())

    cursor_list = collection.find()
    myList = []
    [myList.append(i['nombre']) for i in cursor_list]

    finalStr = "".join(myList)
    return finalStr

@app.route('/eliminar')
def delete_all():
    ok, connection = getMongoClient()
    if not ok:
        return Response(response=json.dumps(connection), mimetype='application/json')
    collection = getCollection(connection,"superheros")
    collection.delete_many({})
    return "SUCCED! DataBase Has been ereased!"
    

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/list_heros', methods=('GET', 'POST'))
def list_heros():
    ok, connection = getMongoClient()
    if not ok:
        return Response(response=json.dumps(connection), mimetype='application/json')
    collection = getCollection(connection,"superheros")
    cursor_list = collection.find()
    return render_template('heros.html', allHeros=cursor_list)

@app.route('/process_hero', methods=['POST'])
def buscar_super_hero():
    miSuperhero = request.json.get('hero')

    url = 'https://gateway.marvel.com/v1/public/characters?'
    public_key = 'yourPublicKey'
    private_key = 'yourPrivateKey'
    ts = str(time.time()).split('.')[0]
    md5_hash = hashlib.md5((ts+private_key+public_key).encode()).hexdigest()

    url = url + 'name='+miSuperhero+ '&ts='+ts + '&apikey='+ public_key + '&hash=' + md5_hash

    response = requests.get(url)
    if response.status_code == 200:

        mihero = response.json()['data']['results'][0]

        nombre = mihero['name']
        descripcion = mihero['description'] or "No description!"
        comics = mihero['comics']['available']
        series = mihero['series']['available']
        historias = mihero['stories']['available']
        eventos = mihero['events']['available']

        miheroClass = Superhero(nombre,descripcion,comics,series,historias,eventos)

    else:
        print(f"Error: {response.status_code}")

    return jsonify({
        'nombre': miheroClass.nombre,
        'descripcion': miheroClass.descripcion,
        'comics': miheroClass.comics,
        'series': miheroClass.series,
        'historias': miheroClass.historias,
        'eventos': miheroClass.eventos
        })

@app.route('/save_hero', methods=['POST'])
def guardar_hero():
    ok, connection = getMongoClient()
    if not ok:
        return Response(response=json.dumps(connection), mimetype='application/json')
    collection = getCollection(connection,"superheros")
    
    mihero = Superhero(**json.loads(request.json))
    collection.insert_one(mihero.toDBCollection())
    return "Superhéroe Guardado!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)