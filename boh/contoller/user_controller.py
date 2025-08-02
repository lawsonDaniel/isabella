from flask_restful import Resource
from flask import request
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserController(Resource):
    
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')  # Use .get to avoid KeyError
        if user_id is None:
            return {
                "message": "User ID not found in token",
                "success": False
            }, 401
        
        user_info = UserService.get_auth_user(user_id)
        if user_info:
            return user_info, 200
        return {
            "message": "User not found",
            "success": False
        }, 404

    @jwt_required()
    def post(self):
        data = request.json
        if not data:
            return {
                "message": "No input data provided",
                "success": False
            }, 400
        return UserService.create_user(data)

    @jwt_required()
    def patch(self):
        data = request.json
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        if user_id is None:
            return {
                "message": "User ID not found in token",
                "success": False
            }, 401
        
        if not data:
            return {
                "message": "No input data provided",
                "success": False
            }, 400

        return UserService.update_user(user_id, data)

    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        if user_id is None:
            return {
                "message": "User ID not found in token",
                "success": False
            }, 401
        
        return UserService.delete_user(user_id)
