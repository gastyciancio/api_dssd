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
        return jsonify({'Error': 'Materials required' })


    suppliers = Supplier.get_suppliers(materiales, filtro_precio, dias_extra)
    suppliers = [ supplier.json() for supplier in suppliers ]

    # Retorno en un arreglo los materiales que no tengan un proveedor asi tenemos registro de los mismos
    materiales_sin_supplier = []
    for material in materiales:
        tiene_supplier= False
        for supplier in suppliers:
            for material_of_supplier in supplier['materials']:
                if (tiene_supplier == True):
                    break
                if (material_of_supplier['name'].lower() == material['name'].lower()):
                    tiene_supplier = True
                    break
        if (tiene_supplier == False):
            materiales_sin_supplier.append(material)

    return jsonify({'suppliers': suppliers, 'metadata':{'materiales_sin_proveedor': materiales_sin_supplier} })