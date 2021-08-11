from create_app import db
import uuid
from datetime import datetime


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