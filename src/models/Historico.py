from models.db import db

class Historico(db.Model):
    __tablename__ = "historico"

    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)
    id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.DECIMAL(5, 2), nullable=True)

    def __init__(self, dados):
        self.id_aluno = dados.get('id_aluno')
        self.id_disciplina = dados.get('id_disciplina')
        self.status = dados.get('status')
        self.ano = dados.get('ano')
        self.semestre = dados.get('semestre')
        self.nota = dados.get('nota')

    def to_json(self) -> dict:
        return {
            "id_aluno": self.id_aluno,
            "id_disciplina": self.id_disciplina,
            "status": self.status,
            "ano": self.ano,
            "semestre": self.semestre,
            "nota": self.nota
        }
