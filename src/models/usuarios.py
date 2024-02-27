from datetime import datetime

from models.db import db
from sqlalchemy import func
from sqlalchemy_utils import EmailType, PasswordType
from passlib.hash import pbkdf2_sha256


class usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Definindo a chave primária
    username = db.Column(db.String(length=100))
    email = db.Column(EmailType())
    password = db.Column(PasswordType(schemes=['pbkdf2_sha256']))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = pbkdf2_sha256.hash(self.password)
        db.session.add(self)
        db.session.commit()

    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.is_admin = is_admin

    def gen_hash(self, password):
        return pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

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
            'username': str(self.username),
            'password': str(self.password),
            'email': str(self.email),
            'is_admin': str(self.is_admin)
        }
