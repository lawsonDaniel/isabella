from sqlalchemy import Column, Integer, ForeignKey, String
from db_config import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)  # Foreign Key to user table
    category = db.Column(String, nullable=False)  # Category field
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships, if any, could be added here
