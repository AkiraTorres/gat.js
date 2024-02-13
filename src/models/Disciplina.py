from src.models.db import db

class Disciplina(db.Model):
    __tablename__ = "disciplina"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer)
    credito = db.Column(db.Integer)
    tipo = db.Column(db.Integer, nullable=False)
    matricula_professor = db.Column(db.Integer, db.ForeignKey('professor.matricula'), nullable=True)

    def __init__(self, dados):
        self.carga_horaria = dados.get("carga_horaria")
        self.codigo = dados.get("codigo")
        self.credito = dados.get("credito")
        self.nome = dados.get("nome")
        self.tipo = dados.get("tipo")
        self.matricula_professor = dados.get("matricula_professor")


    def to_json(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "credito": self.credito,
            "tipo": self.tipo,
            "matricula_professor": self.matricula_professor
        }

