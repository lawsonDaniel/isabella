from flask import redirect
from db_config import db
from models.link_model import Link
from models.user_model import User
from schema.schema import UserSchema, VideoSchema, LinkSchema
from datetime import datetime, timedelta

user_schema = UserSchema()
video_schema = VideoSchema()
link_schema = LinkSchema()

class SubscriptionService:
    
    def subscribe_to_youtube(user_id, ip):
        try:
            subscription_link = "https://www.youtube.com/@BreathOfHopePodcast?sub_confirmation=1"
            
            # Check if a link with this user_id and IP address exists within the last 24 hours
            existing_link = Link.query.filter(
                Link.ip_addresses.contains([ip]),  # Ensure ip_addresses column supports JSONB
                Link.user_id == user_id,
                Link.video_id.is_(None),
                Link.last_click >= datetime.utcnow() - timedelta(hours=24)
            ).first()

            if existing_link:
                # Update last_click for the existing link
                existing_link.last_click = datetime.utcnow()
                db.session.commit()
                return redirect(subscription_link, code=302)

            # If no recent link exists, proceed to create a new one
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return {
                    "message": "User not found",
                    "success": False
                }, 404

            # Increment user points, defaulting to 0 if points are None
            user.point = (user.point or 0) + 3
            db.session.add(user)  # Add user back to session for updates
            db.session.commit()

            # Create and save the new link
            new_link = Link(
                user_id=user_id,
                ip_addresses=[ip],  # Ensure ip_addresses column is defined as JSONB
                last_click=datetime.utcnow()
            )
            db.session.add(new_link)
            db.session.commit()

            return redirect(subscription_link, code=302)

        except SQLAlchemyError as db_error:
            # Handle database-related errors
            return {
                "message": "A database error occurred",
                "success": False,
                "error": str(db_error)
            }, 500

        except Exception as e:
            # Catch any other exceptions
            return {
                "message": "An unexpected error occurred",
                "success": False,
                "error": str(e)
            }, 500
