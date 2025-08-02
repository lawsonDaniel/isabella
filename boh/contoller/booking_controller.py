from flask_restful import Resource
from flask import request
from services.booking_service import BookingService
from flask_jwt_extended import jwt_required, get_jwt_identity

class BookingController(Resource):
    
    def get(self):
        print("reaching here 111")
        return 'working'
        
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

        # Call the static method directly
        return BookingService.create_user_booking(user_id, data)
    
    @jwt_required()
    def get(self):
         page = request.args.get('page', 1, type=int)  # Default page is 1
         per_page = request.args.get('per_page', 10, type=int)  # Default items per page is 10
         search = request.args.get('search', '', type=str) 
         date = request.args.get('date', '', type=str)
         return BookingService.get_all_user_bookings(search,date,page,per_page)
        
  