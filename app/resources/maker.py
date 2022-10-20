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

   # Retorno en un arreglo los materiales que no tengan un proveedor asi tenemos registro de los mismos
    materiales_sin_maker = []
    for material in materiales:
        tiene_maker= False
        for maker in makers:
            for material_of_maker in maker['materials']:
                if (tiene_maker == True):
                    break
                if (material_of_maker['name'].lower() == material['name'].lower()):
                    tiene_maker = True
                    break
        if (tiene_maker == False):
            materiales_sin_maker.append(material)

    return jsonify({'makers': makers, 'metadata':{'materiales_sin_fabricante': materiales_sin_maker} })

@maker.post("/reserve")
@jwt_required()  ###Decorator para proteger la ruta
def reserve():
    consulta = request.json
    makers_consulta = consulta.get("makers")
   

    if makers_consulta == None:
        return jsonify({'Error': 'Makers required' })


    messages = Maker.reserve_makers(makers_consulta)

    return jsonify({'response': messages})