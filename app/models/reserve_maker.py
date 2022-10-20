from sqlalchemy import Column, ForeignKey, Text,String
from app.db import db
from datetime import datetime

class ReserveMaker(db.Model):
    __tablename__ = "reserve_maker"
    maker_id = Column(ForeignKey("maker.id"), primary_key=True, nullable=False)
    date_reserved = Column(String(16), primary_key=True, nullable=False)

    def json(self):
        return {
            'maker_id': self.maker_id,
            'date_reserved': datetime.strptime(self.date_reserved,"%d/%m/%Y").date()
        }
    
    @classmethod
    def get_reserve_makers(cls):
        return ReserveMaker.query.all()
    
    def __init__(self,maker_id=None,date_reserved=None):
        self.maker_id=maker_id
        self.date_reserved=date_reserved