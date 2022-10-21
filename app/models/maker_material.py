from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db import db
from datetime import date, timedelta

class MakerMaterial(db.Model):
    __tablename__ = "maker_material"
    maker_id = Column(ForeignKey("maker.id"), primary_key=True)
    material_id = Column(ForeignKey("material.id"), primary_key=True)
    price_per_kg = Column(Float, nullable=False)
    material = relationship("Material")

    def json(self):
        return {
            'id': self.material.id,
            'name': self.material.name,
            'price_per_kg': self.price_per_kg
        }
    
    @classmethod
    def get_maker_material(cls):
        return MakerMaterial.query.all()
