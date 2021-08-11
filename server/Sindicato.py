from create_app import db
import uuid


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