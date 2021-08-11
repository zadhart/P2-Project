from create_app import db
import uuid

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