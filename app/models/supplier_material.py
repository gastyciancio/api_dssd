from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.models.material import Material
from app.db import db
from datetime import date, timedelta, datetime

class SupplierMaterial(db.Model):
    __tablename__ = "supplier_material"
    supplier_id = Column(ForeignKey("supplier.id"), primary_key=True)
    material_id = Column(ForeignKey("material.id"), primary_key=True)
    amount = Column(Integer)
    price_per_kg = Column(Float, nullable=False)
    days_deliver = Column(Integer)

    material = relationship("Material")

    def json(self):
        return {
            'id': self.material.id,
            'name': self.material.name,
            'price_per_kg': self.price_per_kg,
            'date_deliver': (date.today() + timedelta(days=self.days_deliver)).strftime("%d/%m/%Y")
        }
    
    @classmethod
    def get_supllier_material(cls):
        return SupplierMaterial.query.all()
