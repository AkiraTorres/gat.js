from models.db import db

class Aluno(db.Model):
    __tablename__ = "aluno"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    arg_class = db.Column(db.DECIMAL(5, 2), nullable=False)
    ano_entrada = db.Column(db.Integer, nullable=False)

    def __init__(self, dados):
        self.nome = dados.get("nome")
        self.cpf = dados.get("cpf")
        self.arg_class = dados.get("arg_class")
        self.ano_entrada = dados.get("ano_entrada")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "arg_class": self.arg_class,
            "ano_entrada": self.ano_entrada
        }
