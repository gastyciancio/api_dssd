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
    def get_suppliers(cls, materiales, fecha_deseada):

        lista_suppliers = []
        nombres_materiales = []
        fecha_deseada = datetime.strptime(fecha_deseada,"%d/%m/%Y").date()

        for material in materiales:
            nombres_materiales.append(material['name'].lower())
    
        suppliers = Supplier.query.all()
        for supplier in suppliers:

            lista_materiales = []
            for supplier_material in supplier.materials:

                date_deliver = date.today() + timedelta(days=supplier_material.days_deliver)

                cantidad_material = 999999
                for material in materiales:
                    if (material['name'].lower() == (supplier_material.material.name).lower()):
                        cantidad_material=material['amount']
                        break
                if ((supplier_material.material.name).lower() in nombres_materiales) and (cantidad_material <= supplier_material.amount) and (date_deliver <= fecha_deseada):  
                    lista_materiales.append(supplier_material)
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
      