from flask import Blueprint, jsonify, request
from app.models.supplier import Supplier

supplier = Blueprint("suppliers", __name__, url_prefix="/suppliers")

@supplier.get("/index")
def index():
    suppliers = Supplier.getAll()
    suppliers = [ supplier.json() for supplier in suppliers ]
    return jsonify({'suppliers': suppliers })

@supplier.get("/by_data")
def by_data():
    consulta = request.json
    materiales = consulta.get("materiales")
    filtro_precio = consulta.get("filtro_precio")
    dias_extra = consulta.get("dias_extra")

    if materiales == None:
        return jsonify({'Error': 'Materiales required' })


    suppliers = Supplier.get_suppliers(materiales, filtro_precio,dias_extra)
    suppliers = [ supplier.json() for supplier in suppliers ]
    return jsonify({'suppliers': suppliers })