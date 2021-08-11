from create_app import db
import uuid

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