from models.db import db

class Historico(db.Model):
    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf_aluno = db.Column(db.String(14), db.ForeignKey('aluno.cpf'))  # Alterei de Integer para String para poder fazer a relação com a tabela aluno
    id_disciplina = db.Column(db.Integer, db.ForeignKey('disciplina.id'))
    status = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.DECIMAL(5, 2), nullable=True)

    def __init__(self, dados):
        self.cpf_aluno = dados.get('cpf_aluno')
        self.id_disciplina = dados.get('id_disciplina')
        self.status = dados.get('status')
        self.ano = dados.get('ano')
        self.semestre = dados.get('semestre')
        self.nota = dados.get('nota')

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "cpf_aluno": self.cpf_aluno,
            "id_disciplina": self.id_disciplina,
            "status": self.status,
            "ano": self.ano,
            "semestre": self.semestre,
            "nota": self.nota
        }
