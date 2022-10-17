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

    suppliers = Supplier.get_suppliers(consulta["materiales"])
    suppliers = [ supplier.json() for supplier in suppliers ]
    return jsonify({'suppliers': suppliers })