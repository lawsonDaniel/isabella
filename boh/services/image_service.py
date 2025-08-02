from db_config import db
from models.user_model import User
from utils.upload import upload_image_to_cloudinary
from flask import current_app

class ImageService:
    @staticmethod
    def upload_user_image(user_id, image_link):
        try:
            # Fetch the user from the database
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found", "success": False}, 404

            # Upload the image to Cloudinary
            result = upload_image_to_cloudinary(image_link, public_id=f"user_{user_id}")
            
            if not result['success']:
                return {"message": "Image upload failed", "success": False}, 500

            # Update user's image field with the URL of the uploaded image
            user.image = result['url']
            db.session.commit()

            return {
                "message": "Image uploaded and saved successfully.",
                "success": True,
                "image_url": user.image
            }, 200

        except Exception as e:
            return {
                "message": "An error occurred while uploading the image.",
                "success": False,
                "error": str(e)
            }, 500
