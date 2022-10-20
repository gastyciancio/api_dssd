from sqlalchemy import Column, Integer, Text
from app.db import db
from sqlalchemy.orm import relationship
from app.models.maker_material import MakerMaterial
from datetime import date, timedelta, datetime
from app.models.reserve_maker import ReserveMaker

class Maker(db.Model):
    __tablename__="maker"
    id = Column(Integer,primary_key=True)
    name = Column(Text, nullable=False)
    materials = relationship("MakerMaterial")

    def __init__(self,id=None,name=None,materials=None):
        self.id=id
        self.name=name
        self.materials=materials
    
    @classmethod
    def get_makers(cls):
        return Maker.query.all()

    @classmethod
    def get_makers_filtered(cls, materiales, filtro_precio=None, dias_extra=None):
        
        lista_makers = []
        nombres_materiales = []

        for material in materiales:
            nombres_materiales.append(material['name'].lower())
    
        makers = Maker.query.all()
        for maker in makers:

            lista_materiales = []
            for maker_material in maker.materials:

                date_deliver = date.today() + timedelta(days=maker_material.days_deliver)

                cantidad_material = 999999999
                fecha_deseada = None

                #BUSCAMOS EN EL LISTADO DE MATERIALES QUE NOS DIO EL CLIENTE EL MATERIAL DEL FABRICANTE
                for material in materiales:
                    if (material['name'].lower() == (maker_material.material.name).lower()):
                        cantidad_material = material['amount']
                        fecha_deseada = datetime.strptime(material['date_required'],"%d/%m/%Y").date()

                        # AGREGAMOS MAS DIAS DE TOLERANCIA DEL CLIENTE PARA SU MATERIAL SI ESTA EL PARAMETRO OPCIONAL DE LA RENEGOCIACION
                        if (dias_extra != None):
                            fecha_deseada = fecha_deseada + timedelta(days=dias_extra)
                        break

                # NOS FIJAMOS QUE EL MATERIAL ESTE EN EL LISTADO SOLICITADO, QUE LA CANTIDAD PEDIDA SEA MENOR IGUAL AL STOCK ACTUAL DEL MATERIAL Y QUE LA FECHA QUE ENTREGA EL PROVEEDOR SEA MENOR IGUAL A LA QUE EL CLIENTE DESEA
                if (cantidad_material <= maker_material.max_amount) and (date_deliver <= fecha_deseada):

                    # FILTRO POR PRECIO, PARAMETRO OPCIONAL DE LA RENEGOCIACION
                    if (filtro_precio == None or filtro_precio >= maker_material.price_per_kg):
                        lista_materiales.append(maker_material)
                    
            # SI EXISTE AL MENOS UN MATERIAL SIGINIFICA QUE EL PROVEEDOR ES UTIL PARA LA BUSQUEDA, SE LO AGREGA AL LISTADO DE PROVEEDORES SOLO CON LOS MATERIALES QUE SIRVEN
            if (len(lista_materiales) > 0):
                maker_with_only_materials_asked = Maker(maker.id, maker.name, lista_materiales)
                lista_makers.append(maker_with_only_materials_asked)
        
        return lista_makers

    @classmethod
    def reserve_makers(cls, makers):

        messages = []
        reserved_makers = ReserveMaker.get_reserve_makers()
        for maker in makers:
            
            reservado = False
            fecha = None
            for reserved_maker in reserved_makers:
                if (reserved_maker.maker_id == maker['id']) and (datetime.strptime(reserved_maker.date_reserved,"%d/%m/%Y").date() >= datetime.strptime(maker['date_deliver'],"%d/%m/%Y").date()):
                    reservado = True
                    fecha = reserved_maker.date_reserved
                    break

            if (reservado == True):
                messages.append(
                    {
                        "message":'El fabricante esta ocupado hasta la fecha: ' + fecha,
                        "maker_id": maker['id']
                    })

            else:
                cantidad_pedidos_superan_maximo = 0
                for material in maker['materials']:
                    makermaterial_in_bd = MakerMaterial.query.get((maker['id'], material['id']))
                    if (makermaterial_in_bd.max_amount < material['amount']):
                        cantidad_pedidos_superan_maximo = cantidad_pedidos_superan_maximo + 1
                        messages.append(
                            {
                                "message":"El pedido del cliente supera la cantidad maxima que acepta el fabricante",
                                "maker_id": maker['id'], 
                                'material_id':material['id']
                            })
                if (cantidad_pedidos_superan_maximo == 0):
                    new_reserve = ReserveMaker(maker['id'],maker['date_deliver'])
                    db.session.add(new_reserve)
                    db.session.commit()
                    messages.append(
                            {
                                "message":"El fabricante reservo el espacio",
                                "maker_id": maker['id']
                            })
        return messages


    def json(self):
        materials = [ material.json() for material in self.materials ]

        return {
            'id': self.id,
            'name': self.name,
            'materials' : materials
        }
        