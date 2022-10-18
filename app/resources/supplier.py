from flask import Blueprint, jsonify, request
from app.models.supplier import Supplier
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

supplier = Blueprint("suppliers", __name__, url_prefix="/suppliers")

@supplier.get("/index")
def index():
    suppliers = Supplier.getAll()
    suppliers = [ supplier.json() for supplier in suppliers ]
    return jsonify({'suppliers': suppliers })

@supplier.get("/by_data")
def by_data():
    consulta = request.json

    suppliers = Supplier.get_suppliers(consulta["materiales"], consulta["filtro_precio"],consulta["dias_extra"])
    suppliers = [ supplier.json() for supplier in suppliers ]
    return jsonify({'suppliers': suppliers })

"""
Endpoint para testear el jwt
GET http://localhost:5000/suppliers/protected-test-jwt
Headers: {
    Authorization: Bearer ${jwt sacado del auth, sin comillas}
}
"""
@supplier.get('/protected-test-jwt')
@jwt_required()  ###Decorator para proteger la ruta
def test():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200