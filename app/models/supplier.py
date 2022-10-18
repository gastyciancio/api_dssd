from unittest import case
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.db import db
from datetime import date, timedelta, datetime

class Supplier(db.Model):
    __tablename__="supplier"
    id = Column(Integer,primary_key=True)
    name = Column(Text, nullable=False)
    materials = relationship("SupplierMaterial")

    @classmethod
    def get_suppliers(cls, materiales, filtro_precio, dias_extra):

        lista_suppliers = []
        nombres_materiales = []
        #fecha_deseada = datetime.strptime(fecha_deseada,"%d/%m/%Y").date()

        for material in materiales:
            nombres_materiales.append(material['name'].lower())
    
        suppliers = Supplier.query.all()
        for supplier in suppliers:

            lista_materiales = []
            for supplier_material in supplier.materials:

                date_deliver = date.today() + timedelta(days=supplier_material.days_deliver)

                cantidad_material = 999999
                fecha_deseada = None

                #BUSCAMOS EN EL LISTADO DE MATERIALES QUE NOS DIO EL CLIENTE EL MATERIAL DEL PROVEEDOR
                for material in materiales:
                    if (material['name'].lower() == (supplier_material.material.name).lower()):
                        cantidad_material = material['amount']
                        fecha_deseada = datetime.strptime(material['date_required'],"%d/%m/%Y").date()

                        # AGREGAMOS MAS DIAS DE TOLERANCIA DEL CLIENTE PARA SU MATERIAL SI ESTA EL PARAMETRO OPCIONAL DE LA RENEGOCIACION
                        if (dias_extra != None):
                            fecha_deseada = fecha_deseada + timedelta(days=dias_extra)
                        break
                # NOS FIJAMOS QUE EL MATERIAL ESTE EN EL LISTADO SOLICITADO, QUE LA CANTIDAD PEDIDA SEA MENOR IGUAL AL STOCK ACTUAL DEL MATERIAL Y QUE LA FECHA QUE ENTREGA EL PROVEEDOR SEA MENOR IGUAL A LA QUE EL CLIENTE DESEA
                if ((supplier_material.material.name).lower() in nombres_materiales) and (cantidad_material <= supplier_material.amount) and (date_deliver <= fecha_deseada):

                    # FILTRO POR PRECIO, PARAMETRO OPCIONAL DE LA RENEGOCIACION
                    if (filtro_precio == None):
                        lista_materiales.append(supplier_material)
                    else:
                        if (filtro_precio > supplier_material.price_perk_kg):
                            lista_materiales.append(supplier_material)
                    
            # SI EXISTE AL MENOS UN MATERIAL SIGINIFICA QUE EL PROVEEDOR ES UTIL PARA LA BUSQUEDA, SE LO AGREGA AL LISTADO DE PROVEEDORES SOLO CON LOS MATERIALES QUE SIRVEN
            if (len(lista_materiales) > 0):
                supplier_with_only_materials_asked = Supplier(supplier.id,supplier.name, lista_materiales)
                lista_suppliers.append(supplier_with_only_materials_asked)
        return lista_suppliers
    
    @classmethod
    def getAll(cls):
        return Supplier.query.all()
    
    def json(self):
        materials = [ material.json() for material in self.materials ]

        return {
            'id': self.id,
            'name': self.name,
            'materials' : materials
        }

    def __init__(self,id=None,name=None,materials=None):
        self.id=id
        self.name=name
        self.materials=materials
      