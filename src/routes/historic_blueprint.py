from flask import Blueprint, request, make_response
from models.db import db
from models.Historico import Historico

historic_blueprint = Blueprint('historico', __name__)


# listar historico escolar 
@historic_blueprint.route('/historico', methods=['GET'])
def find_():
    historicos = Historico.query.all()
    response = make_response([historico.to_json() for historico in historicos])
    return response

