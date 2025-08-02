from flask_restful import Resource
from flask import request
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserController(Resource):
    def get(self, user_id=None):
        if user_id:
            return UserService.get_user_by_id(user_id)
        return UserService.get_all_users()

    def post(self):
        data = request.json
        return UserService.create_user(data)
    
    @jwt_required()
    def patch(self):
        data = request.json
        current_user = get_jwt_identity()
        print('id from jwt',current_user)
        return UserService.update_user(current_user['user_id'], data)

    # def delete(self):
    #     return UserService.delete_user(user_id)
