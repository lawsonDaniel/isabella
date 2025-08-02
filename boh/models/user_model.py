from db_config import db
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    otp = db.Column(db.String(120), nullable=False)
    userType = db.Column(db.String(255), nullable=True, default='User')  # Set default userType to 'User'
    otp_expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=30))
    image = db.Column(db.String(255), nullable=True)
    point = db.Column(db.Integer, nullable=True, default=0)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    links = db.relationship('Link', back_populates='user', lazy=True)  # Keep this as it is
    videos = db.relationship('Video', back_populates='user', lazy=True)  # Keep this as it is

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"
