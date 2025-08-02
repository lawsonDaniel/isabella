from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB  # Correct import for JSONB
from db_config import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Link(db.Model):
    __tablename__ = 'links'
    
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)  # Foreign Key
    video_id = db.Column(Integer, ForeignKey('videos.id'), nullable=True)  # Set as nullable
    last_click = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(String, nullable=True)
    # Relationships
    user = db.relationship('User', back_populates='links')
    video = db.relationship('Video', back_populates='links')
    
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    ip_addresses = db.Column(JSONB, nullable=True)  # JSONB for IP addresses

    # Optional: Index on ip_addresses for performance
    __table_args__ = (
        db.Index('ix_links_ip_addresses', 'ip_addresses', postgresql_using='gin'),  # GIN index for JSONB
    )