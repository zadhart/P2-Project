from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projetoP2.sqlite3'
db = SQLAlchemy(app)

# Creating the ORM objects


class Empregado(db.Model):
    id = db.Column(db.String(255), unique=True, primary_key=True)
    endereco = db.Column(db.String(255))
    tipo = db.Column(db.String(255), nullable=False)
    tipoPagamento = db.Column(db.String(255), nullable=False)
    agendaPagamento = db.Column(db.String(255), nullable=False)

    def __init__(self, endereco, tipo, tipoPagamento, agendaPagamento):
        self.id = str(uuid.uuid4())
        self.endereco = endereco
        self.tipo = tipo
        self.tipoPagamento = tipoPagamento
        self.agendaPagamento = agendaPagamento


class Assalariados(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    salario = db.Column(db.Float)


class Horistas(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    horasTrabalhadas = db.Column(db.Float)


class Comissionados(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    salario = db.Column(db.Float, nullable=False)
    comissaoP = db.Column(db.Float, nullable=False)


class Vendas(db.Model):
    vid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.Integer, db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    valor = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False)


class PagSemanal(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    diaSem = db.Column(db.String, nullable=False)


class PagBiSemanal(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    diaSem = db.Column(db.String, nullable=False)
    tipoSem = db.Column(db.String, nullable=False)


class PagMensal(db.Model):
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), primary_key=True, unique=True, nullable=False)
    diaMes = db.Column(db.Integer, nullable=False)


class Sindicato(db.Model):
    sid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id"), unique=True, nullable=False)
    taxa = db.Column(db.Float)
    taxaAdic = db.Column(db.Float)


# Creating the Routes

@app.route("/ADD_EMPLOYEE", methods=["GET", "POST"])
def add_employee():
    content = request.get_json()

    db.session.add(Empregado(
        endereco=content["endereco"],
        tipo=content["tipo"],
        tipoPagamento=content["tipoPagamento"],
        agendaPagamento=content["agendaPagamento"]
    ))
    db.session.commit()

    print("Created new employee")
    return "Created new employee"


if __name__ == '__main__':
    app.run()
