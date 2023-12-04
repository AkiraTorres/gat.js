from models.db import db

class Disciplina(db.Model):
    __tablename__ = "disciplina"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer)
    credito = db.Column(db.Integer)
    tipo = db.Column(db.Integer, nullable=False)

    def __init__(self, codigo, nome, carga_horaria, credito, tipo):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.credito = credito
        self.tipo = tipo

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "credito": self.credito,
            "tipo": self.tipo
        }
