import os
import sys
from dotenv import load_dotenv

sys.path.append('../')
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_ENV = os.getenv("DB_ENV")

class Config:
    DEBUG = False
    DEVELOPMENT = False
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_ENV}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
