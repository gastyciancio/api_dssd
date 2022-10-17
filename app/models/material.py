from sqlalchemy import Column, Integer, Text
from app.db import db

class Material(db.Model):
    __tablename__="material"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    @classmethod
    def get_material(cls):
        return Material.query.all()