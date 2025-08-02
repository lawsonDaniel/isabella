from flask_restful import Resource
from flask import request
from services.image_service import ImageService  

class ImageController(Resource):
    def __init__(self, app):
        self.app = app
        self.image_service = ImageService()  # Pass app to ImageService

    def patch(self, user_id):
        """
        Update the user's profile image.
        Expects JSON body with an 'image' field containing the image link.
        """
        data = request.json
        errors = []

        if not data.get('image'):
            errors.append("The image link is missing.")

        if errors:
            return {
                "message": "Validation failed.",
                "errors": errors,
                "success": False
            }, 400

        # Call the image service to handle the upload
        return self.image_service.upload_user_image(user_id, data['image'])
