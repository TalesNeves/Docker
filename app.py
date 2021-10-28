from logging import error
from re import S
from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import json, jwt

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] ='mysql://user:PASsword123!@#@localhost:3306/main'
app.config["SQLALCHEMY_DATABASE_URI"] ='mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

class Usuario(db.Model):
    # id = db.Column(db.Integer, primary_key=True, auto_increment=False)
    email = db.Column(db.String(200), primary_key=True)
    senha = db.Column(db.String(200))

    def get_objects(self):
        data = {

            'email' : self.email,
            'senha' : self.senha
        }
        return data

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    comprador = db.Column(db.String(200))
    vendedor = db.Column(db.String(200))
    valor = db.Column(db.Float)

    def get_objects(self):
        data = {
            'id' : self.id,
            'titulo' : self.id,
            'comprador' : self.comprador,
            'vendedor' : self.vendedor,
            'valor' : self.valor
            }
        return data




PORT = 3201
HOST = '0.0.0.0'


#GET METHOD

@app.route("/")
def home():
    return render_template('menu.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login")
def login():
    return render_template('login.html')    

@app.route("/products")
def productpage():
    return render_template('produto.html')
@app.route("/home")
def template():
    return render_template('index.html')

@app.route("/decode/<token>")
def decode(token): 
    return make_response(jsonify({"token":jwt.decode(token, "123", algorithms="HS256")}))

@app.route("/authorize", methods=["POST"])
def teste():
    body = request.get_json()
    queryresult = db.session.query(Usuario).filter_by(email=body["email"])
    for row in queryresult:
        if row.senha == body["senha"]:
            token = jwt.encode({"email":body["email"]}, "123", algorithm="HS256")
            return make_response(jsonify({"token":token}),200)
            # return make_response(jsonify({"token":jwt.decode(token, "123", algorithms="HS256")}),201)
        else: 
            return make_response(jsonify({"error":"error"}),401)
        
    return make_response(body,401)
    # res = make_response(jsonify({"usuario":usuario.get_objects()}),200)
    # return res 

  

@app.route("/show")
def showproduct():
    produtos = Produto.query.all()
    # jsonstring = json.dumps([ob.__dict__ for ob in produtos])
    jsonstring = [ ob.get_objects() for ob in produtos]
    print(produtos)
    res = make_response(jsonify({"produtos":jsonstring}),200)
    #res = make_response(jsonify({"produtos":produtos.get_objects()}),200)
    return res


@app.route("/usuario", methods=["POST"]) #ainda n testei, nsei se o methods ta funcionando
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(email=body["email"], senha=body["senha"])
        db.session.add(usuario)
        db.create_all()
        db.session.commit()
        res = make_response(jsonify({"usuario":usuario.get_objects()}),200)
        return res
    except Exception as e:
        print(e)
        return make_response(jsonify({"error":"error"}),417)


@app.route("/produto", methods=["POST"]) #
def cria_produto():
    body = request.get_json()

    try:
        produto = Produto(titulo=body["titulo"],comprador=body["comprador"], vendedor=body["vendedor"], valor = body["valor"])
        db.session.add(produto)
        db.create_all()
        db.session.commit()
        res = make_response(jsonify({"produto":produto.get_objects()}),200)
        return res
    except Exception as e:
        print(e)
        return make_response(jsonify({"error":"error"}),417)


@app.route("/catalogo")
def mostra_catalogo():
    return render_template('tabela.html')

@app.route("/makebid/<id>/<value>", methods=["PUT"])
def make_bid(id,value):
    body = request.get_json()
    queryresult = db.session.query(Produto).filter_by(id=id)
    for row in queryresult:
        if float(value) > row.valor:
            row.valor = float(value)
            row.comprador = body["comprador"]
            db.session.commit()
            return make_response(jsonify({"valor":float(value)},200))
        elif float(value) <= row.valor:
            return make_response(jsonify({"erro":"erro"},304))
    return make_response(jsonify({"erro":"erro"},400))

@app.route("/bid")
def bid():
     return render_template('lance.html')
if  __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT, debug=True)
