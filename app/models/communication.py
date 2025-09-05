from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Message(db.Model):
    """Message model for user-admin communication"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient = relationship("User", foreign_keys=[recipient_id], backref="received_messages")
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    project = relationship("Project", backref="messages")
    
    # Message can have multiple attachments
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")
    
    @property
    def sender_name(self):
        """Get sender name or fallback"""
        return self.sender.name if self.sender else "System"
    
    @property
    def recipient_name(self):
        """Get recipient name or fallback"""
        return self.recipient.name if self.recipient else "System"
    
    def __repr__(self):
        return f'<Message {self.subject}>'


class MessageAttachment(db.Model):
    """Attachments for messages"""
    __tablename__ = 'message_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    message = relationship("Message", back_populates="attachments")
    
    def __repr__(self):
        return f'<MessageAttachment {self.filename}>'


class Invoice(db.Model):
    """Invoice model for project billing"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, paid, overdue, cancelled
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    paid_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = relationship("Project", backref="invoices")
    
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client = relationship("User", backref="invoices")
    
    # Payment relationship
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'


class Payment(db.Model):
    """Payment model for invoice payments"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(100))  # credit_card, bank_transfer, etc.
    transaction_id = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    invoice = relationship("Invoice", back_populates="payments")
    
    def __repr__(self):
        return f'<Payment {self.id} for Invoice {self.invoice_id}>'
