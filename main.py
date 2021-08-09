from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projetoP2.sqlite3'
db = SQLAlchemy(app)
last_changes = []


class Change():
    def __init__(self, new_data, prev_data, change_function, undo_function):
        self.prev_data = prev_data
        self.new_data = new_data
        self.change_function = change_function
        self.undo_function = undo_function

    def rmv_employee(self):
        '''content = request.get_json()

        obj = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()'''
        obj = self.new_data
        db.session.delete(obj)
        db.session.commit()

        return "Employee removed"

    def add_employee(self):
        db.session.add(self.prev_data)
        db.session.commit()

    def undoUpdate(self):
        self.rmv_employee()
        self.add_employee()
        db.session.commit()

        print("updated")
        return "Updated"

    def cancelSell(self):
        '''content = request.get_json()

        obj = db.session.query(Vendas).filter(Vendas.vid == content["vid"]).first()'''
        obj = self.prev_data
        db.session.delete(obj)
        db.session.commit()

        return "Sell canceled"

    def unreadTcard(self):
        '''content = request.get_json()

        obj = db.session.query(Pontos).filter(Pontos.pid == content["pid"]).first()'''
        obj = self.prev_data
        db.session.delete(obj)
        db.session.commit()

        return "Unread Tcard"

    def undo(self):
        if self.undo_function == "rmv_employee":
            self.rmv_employee()

        elif self.undo_function == "cancel_sell":
            self.cancelSell()

        elif self.undo_function == "unread_tcard":
            self.unreadTcard()

        else:
            self.undoUpdate()



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

    last_changes.append(Change(prev_data=None,
                               new_data=new_employee,
                               change_function="add_employee",
                               undo_function="rmv_employee"))

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

    last_changes.append(Change(prev_data=obj,
                               new_data=None,
                               change_function="rmv_employee",
                               undo_function="add_employee"))

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

    last_changes.append(Change(prev_data=sell,
                               new_data=None,
                               change_function="sell",
                               undo_function="cancel_sell"))

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

    last_changes.append(Change(prev_data=card,
                               new_data=None,
                               change_function="read_tcard",
                               undo_function="unread_tcard"))

    db.session.commit()

    print("Added TCARD")
    return "Added TCARD"


@app.route("/UPDATE", methods=["GET", "POST"])
def update():
    content = request.get_json()

    funcionario = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    old_one = funcionario

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

    last_changes.append(Change(prev_data=old_one,
                               new_data=funcionario,
                               change_function="update",
                               undo_function="undo_update"))

    db.session.commit()

    print("updated")
    return "Updated"

@app.route("/UNDO", methods=["GET", "POST"])
def CtrlZ():
    content = request.get_json()
    c = last_changes.pop(0)
    c.undo()

    return "ctrlZ"


if __name__ == '__main__':
    app.run()
