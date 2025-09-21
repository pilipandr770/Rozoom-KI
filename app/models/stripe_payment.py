from app import db
from datetime import datetime
from app.models.base import User

class StripePayment(db.Model):
    """Model for tracking Stripe payment transactions"""
    __tablename__ = 'stripe_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Payment details
    payment_intent_id = db.Column(db.String(255), unique=True)  # Stripe PaymentIntent ID
    checkout_session_id = db.Column(db.String(255), unique=True)  # Stripe Checkout Session ID
    amount = db.Column(db.Float, nullable=False)  # Amount in EUR
    hours_purchased = db.Column(db.Float, nullable=False)  # Number of development hours purchased
    hourly_rate = db.Column(db.Float, nullable=False)  # Rate per hour at time of purchase
    
    # Payment status
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, succeeded, cancelled, failed
    
    # Customer information
    customer_email = db.Column(db.String(255))
    customer_name = db.Column(db.String(255))
    
    # Reference to price package if applicable
    price_package_id = db.Column(db.Integer, db.ForeignKey('price_packages.id', ondelete='SET NULL'), nullable=True)
    
    # Reference to user account if logged in
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('User', backref='stripe_payments')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Additional metadata
    stripe_metadata = db.Column(db.JSON, nullable=True)  # For storing any additional Stripe metadata
    
    def __repr__(self):
        return f'<StripePayment {self.payment_intent_id} ({self.status})>'