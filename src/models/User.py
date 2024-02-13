from src.models.db import db
from sqlalchemy import func

from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PasswordType
from passlib.hash import pbkdf2_sha256


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)  # Definindo a chave primária
    username = db.Column(db.String(length=100))
    email = db.Column(EmailType())
    password = db.Column(PasswordType(schemes=['pbkdf2_sha256']))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.username

# Recebe a senha e criptografa com o algoritmo pbkdf2_sha256, que o hash gerado é salvo no banco de dados
    def save(self, *args, **kwargs):
        self.password = pbkdf2_sha256.hash(self.password)
        super(User, self).save(*args, **kwargs)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.is_admin = is_admin


    #Checa se a senha passada é igual a senha salva no banco de dados
    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # Verifica se o usuário é administrador
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Verifica se o usuário tem permissão para acessar o app. Neste caso, todos os usuários tem permissão
    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


# Classe para gerenciar os usuários
class UserManager(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Cria um usuário administrador com os dados passados
    def create_admin_user(self, username, email, password):
        user = User(username=username, email=email)
        user.password = pbkdf2_sha256.hash(password)
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        return user

    # Cria um usuário administrador com os dados passados
    def check_credentials(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            return user
        return None

    # Cria um usuário comum com os dados passados
    def create_default_user(self, username, email, password):
        user = User(username=username, email=email)
        user.password = pbkdf2_sha256.hash(password)
        user.is_admin = False
        db.session.add(user)
        db.session.commit()
        return user

# Cria um objeto UserManager
objects = UserManager()
