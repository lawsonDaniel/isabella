from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from services.user_service import UserService

class LeaderController(Resource):
    def __init__(self, app):
        self.app = app
        self.user_service = UserService(app)
    
    @jwt_required()
    def get(self):
         current_user = get_jwt_identity()
         user_id = current_user.get('user_id')  # Use .get to avoid KeyError
         page = request.args.get('page', 1, type=int)  # Default page is 1
         per_page = request.args.get('per_page', 10, type=int)  # Default items per page is 10
         search = request.args.get('search', '', type=str) 
         start_date = request.args.get('start_date', '', type=str) 
         end_date  = request.args.get('end_date', '', type=str) 
         return self.user_service.leaderboard(page,per_page,search,user_id,start_date,end_date)


        