import datetime

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
    nome = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255))
    tipo = db.Column(db.String(255), nullable=False)

    # Criando os relacionamentos entre as tabelas
    assalariados = db.relationship("Assalariados", backref="empregado",uselist=False, cascade="all,delete")
    pontos = db.relationship("Pontos", backref="empregado",uselist=False, cascade="all,delete")
    vendas = db.relationship("Vendas", backref="empregado",uselist=False, cascade="all,delete")
    sindicato = db.relationship("Sindicato", backref="empregado",uselist=False, cascade="all,delete")

    def __init__(self,nome, endereco, tipo):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.endereco = endereco
        self.tipo = tipo


class Assalariados(db.Model):
    pid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    comisssaop = db.Column(db.Float)
    salario = db.Column(db.Float)

    def __init__(self, id, salario, comissao):
        self.pid = str(uuid.uuid4())
        self.id = id
        self.salario = salario
        self.comisssaop = comissao


class Pontos(db.Model):
    pid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    horasTrabalhadas = db.Column(db.Float)
    mes = db.Column(db.Integer, nullable=False)
    semana = db.Column(db.Integer, nullable=False)

    def __init__(self, id, horasTrabalhadas, mes, semana):
        self.pid = str(uuid.uuid4())
        self.id = id
        self.horasTrabalhadas = horasTrabalhadas
        self.mes = mes
        self.semana = semana


class Vendas(db.Model):
    vid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    valor = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, valor):
        self.vid = str(uuid.uuid4())
        self.id = id
        self.valor = valor
        self.date = datetime.date


class Sindicato(db.Model):
    sid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    taxa = db.Column(db.Float)
    taxa_add = db.Column(db.Float)

    def __init__(self, id, taxa, taxa_add):
        self.sid = str(uuid.uuid4())
        self.id = id
        self.taxa = taxa
        self.taxa_add = taxa_add


# Creating the Routes

@app.route("/ADD_EMPLOYEE", methods=["GET", "POST"])
def add_employee():
    content = request.get_json()

    new_employee = Empregado(
        endereco=content["endereco"],
        tipo=content["tipo"],
        nome=content["nome"]
    )

    db.session.add(new_employee)

    # Verificando se o novo empregado é assalariado
    if content["tipo"] == "Assalariado":
        newAssal = Assalariados(
            id=new_employee.id,
            salario=int(content["salario"]),
            comissao=float(content["comissao"])
        )
        db.session.add(newAssal)

    # Verificando se o novo empregado faz parte do sindicato
    if content["sindicato"] == "SIM":
        newSind = Sindicato(
            id=new_employee.id,
            taxa=content["taxa"],
            taxa_add=content["taxa_add"]
        )

        db.session.add(newSind)

    db.session.commit()

    print("Created new employee: " + str(new_employee.id))
    return str(new_employee.id)


@app.route("/RMV_EMPLOYEE", methods=["GET", "POST"])
def rmv_employee():
    content = request.get_json()

    obj = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()
    db.session.delete(obj)
    db.session.commit()

    return "Employee removed"


if __name__ == '__main__':
    app.run()
