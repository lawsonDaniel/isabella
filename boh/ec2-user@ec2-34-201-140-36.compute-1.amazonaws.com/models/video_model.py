# Video Model
from db_config import db
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    platform = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(255), unique=True, nullable=False)
    ref = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # # Foreign key to link video to a user
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # # Relationship back to the User
    # user = db.relationship('User', back_populates='videos')

    def __repr__(self):
        return f"Video('{self.title}', '{self.link}')"