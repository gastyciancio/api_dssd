from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.maker import Maker

maker = Blueprint("makers", __name__, url_prefix="/makers")

@maker.get("/index")
@jwt_required()
def index():
    makers = Maker.get_makers()
    makers = [ makers.json() for makers in makers ]
    return jsonify({'makers': makers })

@maker.post("/by_data")
@jwt_required()
def by_data():
    query = request.json
    materiales = query.get("materiales")
    filtro_precio = query.get("filtro_precio")
    dias_extra = query.get("dias_extra")
    if materiales == None:
        return jsonify({'Error': 'Materials required' })

    makers = Maker.get_makers_filtered(materiales, filtro_precio, dias_extra)
    makers = [ maker.json() for maker in makers ]

    return jsonify({'makers': makers})

@maker.post("/reserve")
@jwt_required()  ###Decorator para proteger la ruta
def reserve():
    consulta = request.json
    makers_consulta = consulta.get("makers")
   

    if makers_consulta == None:
        return jsonify({'Error': 'Makers required' })


    messages = Maker.reserve_makers(makers_consulta)

    return jsonify({'response': messages})