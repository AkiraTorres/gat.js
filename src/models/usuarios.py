from models.db import db
from sqlalchemy_utils import EmailType, PasswordType
from passlib.hash import pbkdf2_sha256


class usuarios(db.Model):
    __tablename__ = 'usuarios'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Definindo a chave primária
    username = db.Column(db.String(length=100))
    email = db.Column(EmailType(), primary_key=True)
    senha = db.Column(db.String(length=100, collation='utf8'))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.senha = pbkdf2_sha256.hash(self.senha)
        db.session.add(self)
        db.session.commit()

    def __init__(self, id, username, email, senha, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.senha = pbkdf2_sha256.hash(senha)
        self.is_admin = is_admin

    def gen_hash(self, senha):
        return pbkdf2_sha256.hash(senha)

    def check_password(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def to_json(self):
        return {
            'username': self.username,
            'senha': self.senha,
            'email': self.email,
            'is_admin': self.is_admin
        }
