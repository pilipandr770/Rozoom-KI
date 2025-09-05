from app import db
from datetime import datetime

class PricePackage(db.Model):
    """Model for pricing packages"""
    __tablename__ = 'price_packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Integer, nullable=False)  # Количество часов в пакете
    price_per_hour = db.Column(db.Float, nullable=False)  # Цена за час
    description = db.Column(db.Text)  # Описание пакета
    is_active = db.Column(db.Boolean, default=True)  # Активен ли пакет
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PricePackage {self.name}>'
    
    @property
    def total_price(self):
        """Calculate total price of package"""
        return self.hours * self.price_per_hour
