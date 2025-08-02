from flask_restful import Resource
from flask import request
from services.booking_service import BookingService
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService

class AdminController(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        print('reaching here')
        if user_id is None:
            return {
                "message": "User ID not found in token",
                "success": False
            }, 401
        return UserService.make_admin(data)