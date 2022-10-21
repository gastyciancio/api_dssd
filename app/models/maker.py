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
    max_amount_glasses = Column(Integer, nullable=False)
    days_deliver = Column(Integer)
    materials = relationship("MakerMaterial")
    
    @classmethod
    def get_makers(cls):
        return Maker.query.all()

    @classmethod
    def get_makers_filtered(cls, materiales, fecha_fabricacion_deseada,amount_glasses, filtro_precio=None, dias_extra=None):
        
        lista_makers = []
        nombres_materiales = []
        fecha_deseada = datetime.strptime(fecha_fabricacion_deseada,"%d/%m/%Y").date()
        if (dias_extra != None):
            fecha_deseada = fecha_deseada + timedelta(days=dias_extra)

        for material in materiales:
            nombres_materiales.append(material['name'].lower())
    
        makers = Maker.query.all()
        for maker in makers:

            lista_materiales = []
            date_deliver = date.today() + timedelta(days=maker.days_deliver)
            for maker_material in maker.materials:

                # NOS FIJAMOS QUE EL MATERIAL ESTE EN EL LISTADO SOLICITADO, QUE LA CANTIDAD PEDIDA SEA MENOR IGUAL AL STOCK ACTUAL DEL MATERIAL Y QUE LA FECHA QUE ENTREGA EL PROVEEDOR SEA MENOR IGUAL A LA QUE EL CLIENTE DESEA
                if (amount_glasses <= maker.max_amount_glasses) and (date_deliver <= fecha_deseada):

                    # FILTRO POR PRECIO, PARAMETRO OPCIONAL DE LA RENEGOCIACION
                    if (filtro_precio == None or filtro_precio >= maker_material.price_per_kg):
                        lista_materiales.append(maker_material)
                    
            # SI EXISTE AL MENOS UN MATERIAL SIGINIFICA QUE EL PROVEEDOR ES UTIL PARA LA BUSQUEDA, SE LO AGREGA AL LISTADO DE PROVEEDORES SOLO CON LOS MATERIALES QUE SIRVEN
            if (len(lista_materiales) > 0):
                materials = [ material.json() for material in lista_materiales ]
                maker_with_only_materials_asked = {
                                                    'id': maker.id,
                                                    'name': maker.name,
                                                    'materials' : materials,
                                                    'date_deliver': datetime.strftime(date_deliver,"%d/%m/%Y")
                                                    }
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
                maker_in_db=Maker.query.get(maker['id'])
                if (maker['amount_glasses'] > maker_in_db.max_amount_glasses):
    
                    messages.append(
                        {
                            "message":"El pedido del cliente supera la cantidad maxima que acepta el fabricante: " + str(maker_in_db.max_amount_glasses),
                            "maker_id": maker['id']
                        })
                else:
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
        