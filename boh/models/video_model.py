from db_config import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    platform = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(255), unique=True, nullable=True)
    ref = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign Key

    user = db.relationship('User', back_populates='videos')  # This is correct
    links = db.relationship('Link', back_populates='video')  # Ensure this is here

    def __repr__(self):
        return f"Video('{self.title}', '{self.link}')"
