from models.db import db

class Professor(db.Model):
    __tablename__ = 'professor'
    matricula = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)

    def __init__(self, dados):
        self.matricula = dados.get('matricula')
        self.nome = dados.get('nome')
        self.cpf = dados.get('cpf')

    def to_json(self) -> dict:
        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "cpf": self.cpf
        }