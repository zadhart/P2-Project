from create_app import db
import uuid
from datetime import datetime


class Vendas(db.Model):
    vid = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(255), db.ForeignKey("empregado.id", ondelete='CASCADE'))
    valor = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    dia = db.Column(db.Integer, nullable=False)

    def __init__(self, id, valor, mes, semana, dia):
        self.vid = str(uuid.uuid4())
        self.id = id
        self.valor = valor
        self.date = datetime.now()
        self.mes = mes
        self.semana = semana
        self.dia = dia