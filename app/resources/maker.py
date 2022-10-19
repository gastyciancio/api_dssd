from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.maker import Maker

maker = Blueprint("makers", __name__, url_prefix="/makers")

@maker.get("/")
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

    makers = Maker.get_makers_filtered(materiales, filtro_precio, dias_extra)
    makers = [ maker.json() for maker in makers ]

    return jsonify({'makers': makers})