from datetime import datetime
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

    # Criando os relacionamentos entre as tabelas
    pontos = db.relationship("Pontos", backref="empregado", uselist=False, cascade="all,delete")
    vendas = db.relationship("Vendas", backref="empregado", uselist=False, cascade="all,delete")
    sindicato = db.relationship("Sindicato", backref="empregado", uselist=False, cascade="all,delete")
    pagamento = db.relationship("Pagamentos", backref="empregado", uselist=False, cascade="all,delete")

    def __init__(self, nome, endereco):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.endereco = endereco


class Pagamentos(db.Model):
    pid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    tipo = db.Column(db.String(255), nullable=False)
    diaMes = db.Column(db.Integer)
    diaSem = db.Column(db.String(255))
    tipoSem = db.Column(db.String(255))
    salario = db.Column(db.Float)
    comissao = db.Column(db.Float)
    salarioHora = db.Column(db.Float)

    def __init__(self, id, tipo, diaMes, diaSem, tipoSem, salario, comissao, salarioHora):
        self.pid = str(uuid.uuid4())
        self.id = id
        self.tipo = tipo
        self.diaMes = diaMes
        self.diaSem = diaSem
        self.tipoSem = tipoSem
        self.salario = salario
        self.salarioHora = salarioHora
        self.comissao = comissao


class Pontos(db.Model):
    pid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    horasTrabalhadas = db.Column(db.Float)
    mes = db.Column(db.Integer, nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, horasTrabalhadas, mes, semana):
        self.pid = str(uuid.uuid4())
        self.id = id
        self.horasTrabalhadas = horasTrabalhadas
        self.mes = mes
        self.semana = semana
        self.date = datetime.now()


class Vendas(db.Model):
    vid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    valor = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, valor):
        self.vid = str(uuid.uuid4())
        self.id = id
        self.valor = valor
        self.date = datetime.now()


class Sindicato(db.Model):
    sid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    membro = db.Column(db.String(255), nullable=False)
    taxa = db.Column(db.Float)
    taxa_add = db.Column(db.Float)

    def __init__(self, id, taxa, taxa_add, membro):
        self.sid = str(uuid.uuid4())
        self.id = id
        self.taxa = taxa
        self.taxa_add = taxa_add
        self.membro = membro


# Creating the Routes

@app.route("/ADD_EMPLOYEE", methods=["GET", "POST"])
def add_employee():
    content = request.get_json()

    new_employee = Empregado(
        endereco=content["endereco"],
        nome=content["nome"]
    )

    db.session.add(new_employee)

    newSind = Sindicato(
        id=new_employee.id,
        membro= content["sindicato"],
        taxa=content["taxa"],
        taxa_add=content["taxa_add"]
    )

    db.session.add(newSind)

    # Estabelecendo o tipo de pagamento do funcionario
    tipoPagam = Pagamentos(
        id=new_employee.id,
        tipo=content["tipo"],
        diaMes=content["diaMes"],
        diaSem=content["diaSem"],
        tipoSem=content["tipoSem"],
        salario=content["salario"],
        comissao=content["comissao"],
        salarioHora=content["salarioHora"]
    )
    db.session.add(tipoPagam)

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


@app.route("/SELL", methods=["GET", "POST"])
def sell():
    content = request.get_json()

    sell = Vendas(
        id=content["id"],
        valor=content["valor"]
    )

    db.session.add(sell)
    db.session.commit()

    print("Created sale")

    return "Created sale"


@app.route("/TCARD", methods=["GET", "POST"])
def read_tcard():
    content = request.get_json()

    card = Pontos(
        id=content["id"],
        horasTrabalhadas=content["horasTrabalhadas"],
        mes=content["mes"],
        semana=content["semana"]
    )

    db.session.add(card)
    db.session.commit()

    print("Added TCARD")
    return "Added TCARD"


@app.route("/UPDATE", methods=["GET", "POST"])
def update():
    content = request.get_json()

    funcionario = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    funcionario.endereco = content["endereco"]

    funcPagamento = db.session.query(Pagamentos).filter(Pagamentos.id == content["id"]).first()

    funcPagamento.tipo = content["tipo"]
    funcPagamento.diaMes = content["diaMes"]
    funcPagamento.diaSem = content["diaSem"]
    funcPagamento.tipoSem = content["tipoSem"]
    funcPagamento.salario = content["salario"]
    funcPagamento.salarioHora = content["salarioHora"]
    funcPagamento.comissao = content["comissao"]

    funcSindicato = db.session.query(Sindicato).filter(Sindicato.id == content["id"]).first()

    funcSindicato.taxa = content["taxa"]
    funcSindicato.taxa_add = content["taxa_add"]
    funcSindicato.membro = content["sindicato"]

    db.session.commit()

    print("updated")
    return "Updated"


if __name__ == '__main__':
    app.run()
